import re, time
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Employee, Visitor
from .forms import VisitorForm, EmployeeForm, EmployeePunchingForm
from .filters import VisitorFilter
from django.core.mail import EmailMultiAlternatives
from .functions import *
import json
from re import search
from twilio.rest import Client as twClient
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
# from termsandconditions.decorators import terms_required


# Common variables used throughout the code
today = timezone.localdate()
status_true = True
status_false = False

# Get all visitors and employees of today's date
vis_today = Visitor.objects.all().filter(date=today)
emp_today = Employee.objects.all().filter(status=True)

# Twilio client object using the ACCOUNT_SID and AUTH_TOKEN from the settings
client = twClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN)


@login_required
def vis__emp(request):
	"""
	View for the main dashboard, where user can choose to check in visitors or check out employees.
	"""
	parameters = {'title': 'Visitors', 'vis': '1'}
	template = 'visitor_management/vm_home.html'
	return render(request, template, parameters)


@login_required
def vis__emp_manager(request):
	"""
	View for handling the check in/out of visitors and employees.
	If the request method is POST, check if it is for checking in visitors or checking out employees.
	Redirect to the appropriate view.
	"""
	if request.method == 'POST':
		if 'vis' in request.POST:
			return redirect('vm-visitors')
		elif 'emp' in request.POST:
			return redirect('vm-employees')
	else:
		return redirect('vm-vis__emp')




@login_required
def visitors(request):
	# Set the title of the page and define which link is active in the navigation bar
	parameters = {'title': 'Visitors', 'vis': '1'}
	template = 'visitor_management/visitors.html'

	# Render the template using the defined parameters
	return render(request, template, parameters)





@login_required
def visitor_manager(request):

	# Check if the request method is a POST request
	if request.method == 'POST':

		# Check if the 'Check In' button is clicked
		if 'in' in request.POST:
			# Create a form object for visitor check-in
			form = VisitorForm()

			# Define the template parameters, including the title, which link is active in the navigation bar, and which form is to be displayed
			parameters = {'form': form, 'title': 'Entry', 'vis': '2', 'vEntry': '1'}
			template = 'visitor_management/visitorIn_form.html'

			# Render the template using the defined parameters
			return render(request, template, parameters)


		# Check if the 'Check Out' button is clicked
		elif 'out' in request.POST:
			# Create a form object for visitor check-out
			form = VisitorForm()

			# Define the template parameters, including the title, which link is active in the navigation bar, and which form is to be displayed
			parameters = {'form': form, 'title': 'Exit', 'vis': '3', 'vExit': '1'}
			template = 'visitor_management/search_form.html'

			# Render the template using the defined parameters
			return render(request, template, parameters)
	# If the request method is not POST, redirect to the visitors page
	else:
		return redirect('vm-visitors')




def terms(request):
	# Render the terms and conditions template
	return render(request, 'visitor_management/termsandconditions.html', {})





@login_required
# @terms_required
def visitor_in(request):
	# If the employee name field is empty, the visiting variable is assigned an empty string
	if not request.POST['emp_name']:
		visiting = ''
	else:
		# If the employee name field is not empty, the visiting variable is assigned a queryset
		# that retrieves the employee with the name equal to the one in the POST request
		visiting = emp_today.get(emp_name=request.POST['emp_name'])
		# Converts the queryset to a dictionary
		visiting = vars(visiting)

	# Instantiating the VisitorForm with the POST data from the request or None if the request method is not POST
	form = VisitorForm(request.POST or None)
	# If the request method is POST
	if request.method == 'POST':

		# If the form is valid
		if form.is_valid():
			# Setting the form's status field to True
			form.instance.status = True
			# Creating an instance of the form without committing it to the database
			instance = form.save(commit=False)
			# Setting the form's admin field to the current user
			instance.admin = request.user
			# Committing the form to the database
			instance.save()

			# Twilio credentials
			account_sid = '{TWILIO SID}'
			auth_token = '{TWILIO AUTH TOKEN}'
			# Instantiating the Twilio client
			client = twClient(account_sid, auth_token)

			# If the visiting variable is not empty
			if not visiting:
				pass
			else:
				# Sending a message to the employee with the name equal to the one in the POST request
				message = client.messages.create(
				# Body of the message with the visitor's name and the purpose of the visit
				body=f"Dear {visiting['emp_name']}, {instance.vis_name} has just checked in. He/she has requested a meeting with you",
				# Receiving phone number with the international code
				to=f"+356{visiting['emp_mob']}",
				# Sender name
				from_="NBTS MT",
				)

			# Try-except block to catch errors when sending the message
			try:
				# Prints the SID of the sent message
				print(twClient.messages.sid)
			except (RuntimeError, TypeError, NameError, AttributeError):
				pass

			# Success message to be displayed to the user
			message = 'Welcome. Please Enter'
			# Adds the success message to the request using the messages framework
			messages.success(request, message)
			# Redirects the user to the vm-vis__emp view
			return redirect('vm-vis__emp')

			# Success message to be displayed to the user
			message = 'Welcome. Please Enter'
			# Adds the success message to the request using the messages framework
			messages.success(request, message)
			# Redirects the user to the vm-vis__emp view
			return redirect('vm-vis__emp')

		# Error message to be displayed if form validation fails
		else:
			message = 'Error!! Please try again!!'
			messages.error(request, message)
			return redirect('vm-vis_manager')

	# Render the template with the form if request method is not POST
	parameters = {'form': form, 'title': 'Entry', 'vis': '3', 'vEntry': '2'}
	template = "visitor_management/visitorIn_form.html"
	return render(request, template, parameters)


def visitor_search(request):
    """
    This function performs the search for the visitor.
    It filters the records of visitors present today with the help of "term"
    from the GET request and returns a JSON response with the visitor name and id.
    """
    form = VisitorForm()
    if 'term' in request.GET:
        # Get the search term from the GET request
        query = request.GET.get('term')

        # Filter the visitors present today with the matching name and status is True
        queryset = vis_today.filter(status=True, vis_name__istartswith=query)

        # Extract the values from the queryset
        response_content = list(queryset.values())

        # Create a list of visitor names and ids
        mylist = list()
        mylist += [vis['vis_name'] + '; ' + vis['vis_id'] for vis in response_content]

        # Return the JSON response with the visitor names and ids
        return JsonResponse(mylist, safe=False)

    # Render the search form template with the form, title, vis, and vExit parameters
    template = 'visitor_management/search_form.html'
    parameters = {'form': form, 'title': 'Exit', 'vis': '4', 'vExit': '2'}
    return render(request, template, parameters)


@login_required
def visitor_out(request):
    """
    This function performs the visitor exit process.
    It splits the visitor name and id from the POST request,
    retrieves the visitor details and render the visitor out form template
    with the visitor details.
    """
    # Split the visitor name and id from the POST request
    my_name, my_id = split_post(request.POST['vis_name'])

    # Retrieve the visitor details with the matching name, id and status is True
    visitor = vis_today.get(status=True, vis_name=my_name, vis_id=my_id)

    # Render the visitor out form template with the visitor details, title, vis, and vExit parameters
    parameters = {
        'visitor': visitor,
        'title': 'Exit',
        'vis': '5',
        'vExit': '3'
    }
    template = 'visitor_management/visitorOut_form.html'
    return render(request, template, parameters)



@login_required
def vis_save_exit(request, pk):
    """
    This function updates the visitor status to False when the visitor checks out.

    Inputs:
    - request: An HttpRequest instance which contains details of the user's request.
    - pk: primary key of the visitor record to be updated.

    Outputs:
    - Redirects to 'vm-vis__emp' with a success message if the visitor status is successfully updated.
    - Redirects to 'vm-vis_search' with an error message if there was an error updating the visitor status.
    """

    visitor = vis_today.get(id=pk)

    if request.method == 'POST':
        # Check if 'exit' is in the request.POST data.
        if 'exit' in request.POST:
            # Set the visitor status to False
            visitor.status = False
            visitor.save()
            # Add a success message
            message = 'Thank you for your Visit. Have a nice day'
            messages.success(request, message)
            # Redirect to the 'vm-vis__emp' page
            return redirect('vm-vis__emp')
        else:
            # Add an error message
            message = 'Error!! Please try again!!'
            messages.error(request, message)
            # Redirect to the 'vm-vis_search' page
            return redirect('vm-vis_search')

@login_required
def employees(request):
    """
    This function returns the employees page.

    Inputs:
    - request: An HttpRequest instance which contains details of the user's request.

    Outputs:
    - Renders the 'visitor_management/employees.html' template with the title 'Employee' and 'emp': '1' in the context.
    """

    parameters = {'title': 'Employee', 'emp': '1'}
    template = 'visitor_management/employees.html'
    return render(request, template, parameters)



@login_required
def employee_manager(request):
	"""
	This view handles the behavior of the employee management form based on the request method.
	It opens either the check-in form or the check-out form.
	"""

	# Check if the request method is POST.
	if request.method == 'POST':
		# Check if the 'Check In' button is clicked.
		if 'in' in request.POST:
			# Create a new form instance of EmployeePunchingForm.
			form = EmployeePunchingForm()

			# Set the parameters for the template to render.
			parameters = {'form': form, 'title': 'Entry', 'emp': '2', 'eEntry': '1'}
			template = 'visitor_management/employee_form.html'

			# Render the template and return the response.
			return render(request, template, parameters)

		# Check if the 'Check Out' button is clicked.
		elif 'out' in request.POST:
			# Create a new form instance of EmployeePunchingForm.
			form = EmployeePunchingForm()

			# Set the parameters for the template to render.
			parameters = {'form': form, 'title': 'Exit', 'emp': '3', 'eExit': '1'}
			template = 'visitor_management/employeeOut_form.html'

			# Render the template and return the response.
			return render(request, template, parameters)
	else:
		# If the request method is not POST, redirect to the 'vm-vis__emp' URL.
		return redirect('vm-vis__emp')


def employee_search(request):
    """
    This function is responsible for returning a list of employees whose name starts with the given query.
    The list is returned as a JSON response.
    """

    # Create an instance of EmployeeForm
    form = EmployeeForm()

    # If a 'term' is provided in the GET request
    if 'term' in request.GET:
        # Get the value of the 'term'
        query = request.GET.get('term')

        # Filter the Employee objects whose name starts with the query
        queryset = Employee.objects.all().filter(emp_name__istartswith=query).distinct()

        # Convert the queryset into a list of dictionaries
        response_content = list(queryset.values())

        # Create a list of strings from the dictionaries, where each string is the name and id of an employee
        mylist = list()
        mylist += [emp['emp_name'] + '; ' + emp['emp_id'] for emp in response_content]

        # Return the list of strings as a JSON response
        return JsonResponse(mylist, safe=False)

    # If no 'term' is provided, return the form
    parameters = {'form': form}
    template = 'visitor_management/employee_form.html'
    return render(request, template, parameters)


def present_employee_search(request):
    """
    A view function to handle the employee search functionality.
    If 'term' is present in the GET request, it filters all the Employees in the database who are present
    (status=True) and whose name starts with the query term.
    Returns a JsonResponse containing a list of employee names that match the criteria.
    """
    if 'term' in request.GET:
        # Get the search term from the GET request
        query = request.GET.get('term')
        # Filter all employees with a status of True (i.e. present)
        queryset = Employee.objects.all().filter(status=True)
        # Further filter the queryset to include only employees whose name starts with the search term (case-insensitive)
        queryset = queryset.filter(emp_name__istartswith=query).distinct()
        # Get the values of the filtered queryset as a list of dictionaries
        response_content = list(queryset.values())
        # Create a list of employee names from the response content
        mylist = [emp['emp_name'] for emp in response_content]

        return JsonResponse(mylist, safe=False)

@login_required
def employee_in(request):
    """
    A view function to handle the employee check-in functionality.
    Requires the user to be logged in.
    Splits the posted employee name and ID into separate variables, and retrieves the corresponding employee from the database.
    If the request method is POST and 'enter' is present in the POST data, the employee's status is set to True and saved to the database.
    A success message is displayed and the user is redirected to the vm-vis__emp view.
    If the request method is POST but 'enter' is not present in the POST data, an error message is displayed and the user is redirected to the vm-empIN view.
    """
    # Split the posted employee name and ID into separate variables
    my_name, my_id = split_post(request.POST['emp_name'])
    # Retrieve the employee from the database based on their name and ID
    employee = Employee.objects.all().get(emp_name=my_name, emp_id=my_id)

    if request.method == 'POST':
        # Check if 'enter' is present in the POST data
        if 'enter' in request.POST:
            # Set the employee's status to True and save the changes to the database
            employee.status = True
            employee.save()
            # Display a success message and redirect to the vm-vis__emp view
            message = 'Welcome. Have a nice day'
            messages.success(request, message)
            return redirect('vm-vis__emp')
        else:
            # Display an error message and redirect to the vm-empIN view
            message = 'Error!! Please try again!!'
            messages.error(request, message)
            return redirect('vm-empIN')



@login_required
def employee_out(request):
    """
    This view handles the process of checking an employee out of the office.
    This view requires a user to be logged in.

    This function is triggered when a user submits a form on the "vm-empOUT" page.
    If the form submission is successful, the employee's status is updated to "False",
    indicating that they are no longer in the office.
    A success message is displayed to the user.

    If the form submission is not successful, an error message is displayed.

    Args:
        request: a request object that contains the form data that was submitted.

    Returns:
        If the form submission is successful, the user is redirected to the "vm-vis__emp" page.
        If the form submission is not successful, the user is redirected to the "vm-empOUT" page.
    """
    # Get the name and id of the employee from the form data
    my_name, my_id = split_post(request.POST['emp_name'])
    # Get the employee from the queryset of employees who are currently in the office
    employee = emp_today.get(emp_name=my_name, emp_id=my_id)

    if request.method == 'POST':
        # Check if the form submission was triggered by the "exit" button
        if 'exit' in request.POST:
            # Update the employee's status to False, indicating they are no longer in the office
            employee.status = False
            employee.save()
            # Display a success message to the user
            message = 'Thank you. Have a nice rest of the day'
            messages.success(request, message)
            # Redirect the user to the "vm-vis__emp" page
            return redirect('vm-vis__emp')
        else:
            # Display an error message if the form submission was not successful
            message = 'Error!! Please try again'
            messages.error(request, message)
            # Redirect the user back to the "vm-empOUT" page
            return redirect('vm-empOUT')



@login_required
def sos(request):
    """
    Function to send an emergency evacuation message to all employees and visitors present on the premises.
    """

    # Default message recipient
    name = "Sir/Madame"
    # Message body with the recipient's name
    body = f"Dear {name}, due to a sudden emergency, you are kindly requested to evacuate the building"

    # Get all employees present on the premises
    emp_prem = Employee.objects.all().filter(status=True)
    # Loop through each employee
    for emp in emp_prem:
        name = emp.emp_name
        # Try sending the message to each employee
        try:
            message_twilio = client.messages.create(
                body=body,
                from_="NBTS MT",
                to=f"+356{emp.emp_mob}",
            )
            # Sleep for 1 second between sending messages to avoid sending too many messages at once
            time.sleep(1)
        except:
            # Pass if sending the message to the employee fails
            pass

    # Get all visitors present on the premises
    vis_prem = Visitor.objects.all().filter(date=today, status=True)
    # Loop through each visitor
    for vis in vis_prem:
        name = vis.vis_name
        # Try sending the message to each visitor
        try:
            message_twilio = client.messages.create(
                body=body,
                from_="NBTS MT",
                to=f"+356{vis.vis_mob}",
            )
            # Sleep for 1 second between sending messages to avoid sending too many messages at once
            time.sleep(1)
        except:
            # Pass if sending the message to the visitor fails
            pass

    # Redirect the user to the roll call page after sending the messages
    return redirect('use__roll_call')
