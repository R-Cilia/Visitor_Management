from django.shortcuts import render, redirect # import render() and redirect() functions from django.shortcuts module
from django.contrib import messages # import messages from django.contrib to display success or error messages
from django.contrib.auth.decorators import login_required # import login_required decorator to protect views that require login
from .forms import UserRegisterForm, UserUpdateForm, SosForm # import UserRegisterForm, UserUpdateForm, SosForm from forms.py in the same directory
from .models import Sos # import Sos model from models.py in the same directory
from visitor_management.models import Visitor, Employee # import Visitor and Employee models from visitor_management app's models.py
from visitor_management.forms import VisitorForm, EmployeeForm # import VisitorForm and EmployeeForm from visitor_management app's forms.py

from django.views.generic import (
	ListView,
	CreateView,
	DetailView,
	UpdateView,
	DeleteView,
	) # import various generic views from django.views.generic
from django.contrib.messages.views import SuccessMessageMixin # import SuccessMessageMixin to display success messages on successful form submission
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # import LoginRequiredMixin and UserPassesTestMixin to protect views that require login
from django.utils import timezone # import timezone to work with time related operations
from django.http import HttpResponse, HttpResponseRedirect # import HttpResponse and HttpResponseRedirect to handle HTTP responses
from django.urls import reverse # import reverse to generate URL for a given view
import csv # import csv module to read and write CSV files
from django.core.exceptions import ObjectDoesNotExist # import ObjectDoesNotExist to handle exception when object does not exist

today = timezone.localdate() # store today's date in local timezone in today variable
vis_today = Visitor.objects.all().filter(date=today) # store all visitor objects with today's date
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def home(request):
	# redirect to login page
	return redirect('use-login')


def register(request):
	"""
	Handles user registration.
	If the request method is POST, the form is bound with the request data and checked for validity.
	If the form is valid, the user is saved and a success message is displayed.
	If the form is not valid, an error message is displayed.
	If the request method is not POST, an empty form is rendered.
	"""
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You can now Log in.')
			return redirect('use-logout')
		else:
			messages.error(request, 'ERROR!!')
	else:
		form = UserRegisterForm()

	return render(request, 'users/register.html', {'form': form})



@login_required
def profile(request):
	"""
	This view function is used to show the profile of the logged-in user and allow them to update their information.
	"""
	if request.method == "POST":
		# Get the instance of the logged-in user to pre-fill the form
		u_form = UserUpdateForm(request.POST, instance=request.user)

		# Check if the form is valid
		if u_form.is_valid():
			# Save the changes made to the form
			u_form.save()
			messages.success(request, f'Your account has been updated')
			# Redirect the user to the profile page
			return redirect('use-profile')
	else:
		# Get the instance of the logged-in user to pre-fill the form
		u_form = UserUpdateForm(instance=request.user)

	# Prepare the context data to be passed to the template
	context = {
		'owner': '1',
		'u_form': u_form,
	}

	# Render the profile template
	return render(request, 'users/profile.html', context)

def dashboard(request):
	"""
	This view function is used to display the dashboard page.
	"""
	# Prepare the context data to be passed to the template
	context = {'dash': '1', 'owner': '1'}

	# Render the dashboard template
	return render(request, 'users/dashboard.html', context)

class DashboardListView(ListView):
	"""
	This class-based view is used to show a list of employees registered by the logged-in user.
	"""
	model = Employee
	template_name = 'users/dashboard_employees.html'

	def get_queryset(self):
		"""
		This function returns the queryset of employees registered by the logged-in user.
		"""
		# Get the queryset from the parent class
		queryset = super().get_queryset()
		return queryset.filter(admin=self.request.user)

	def get_context_data(self, **kwargs):
		"""
		This function is used to add extra data to the context before passing it to the template.
		"""
		# Get the context data from the parent class
		context = super().get_context_data(**kwargs)
		# Add the employees list to the context
		context['employees'] = self.object_list.filter(status=True)
		context["owner"] = '2'
		context['dash'] = '2'
		return context




class DashboardDetailView(DetailView):
	"""Class based view to show the detail of an employee"""
	model = Employee
	template_name = 'users/employee_detail.html'

	def get_context_data(self, **kwargs):
		"""Add additional context data to be passed to the template"""
		context = super().get_context_data(**kwargs)
		context["owner"] = '2'
		context['dash'] = '3'
		return context


class DashboardCreateView(LoginRequiredMixin, CreateView):
	"""Class based view to create a new employee instance"""
	model = Employee
	template_name = 'users/employee_form.html'
	context_object_name = 'form'
	fields = ['emp_name', 'emp_id', 'emp_mob', 'emp_email', 'date', 'check']

	def get_context_data(self, **kwargs):
		"""Add additional context data to be passed to the template"""
		context = super().get_context_data(**kwargs)
		# context['profile'] = self.request.user.id
		context["owner"] = '2'
		context['dash'] = '4'
		return context

	def form_valid(self, form):
		"""Save the new employee instance to the database and set the admin field to the current user"""
		self.object = form.save(commit=False)
		self.object.admin = self.request.user
		self.object.save()
		self.pk = self.object.pk
		return super(DashboardCreateView, self).form_valid(form)

	def get_success_url(self):
		"""Return the URL to redirect to after successfully creating a new employee instance"""
		return reverse('use-dashboard_detail', kwargs={'pk': self.pk})


class DashboardUpdateView(LoginRequiredMixin, UpdateView):
    """Class based view for updating the employee data."""

    # model for the view
    model = Employee

    # template for the view
    template_name = 'users/employee_update.html'

    # fields to be shown in the form
    fields = ['emp_name', 'emp_id', 'emp_mob', 'emp_email']

    def get_context_data(self, **kwargs):
        """Add additional data to the context."""
        context = super().get_context_data(**kwargs)
        context["owner"] = '2'
        context['dash'] = '5'
        return context


class DashboardDeleteView(LoginRequiredMixin, DeleteView):
    """Class based view for deleting an employee data."""

    # model for the view
    model = Employee

    # template for the view
    template_name = 'users/employee_confirm_delete.html'

    # URL to redirect after deletion
    success_url = '/dashboard/'

    def get_context_data(self, **kwargs):
        """Add additional data to the context."""
        context = super().get_context_data(**kwargs)
        context["owner"] = '2'
        context['dash'] = '6'
        return context



class DashboardVisitorListView(ListView):
    """
    A class-based view for displaying the list of visitors for a specific date and user.
    """
    model = Visitor
    template_name = 'users/dashboard_visitors.html'

    def get_queryset(self):
        """
        Returns a queryset filtered by the current user and date.
        """
        queryset = super().get_queryset()
        return queryset.filter(admin=self.request.user, date=today)

    def get_context_data(self, **kwargs):
        """
        Adds the list of visitors and some context variables to the context.
        """
        context = super().get_context_data(**kwargs)
        context['visitors'] = self.object_list.filter(status=True)
        context["owner"] = '2'
        context['dash'] = '7'
        return context

@login_required
def roll_call(request):
    """
    A function-based view for displaying the list of employees and visitors for a specific date.
    """
    try:
        # Get the list of visitors and employees with a specific status and date
        vis = Visitor.objects.all().filter(date=today, status=True)
        emp = Employee.objects.all().filter(status=True)
    except ObjectDoesNotExist:
        vis = 0
        emp = 0

    parameters = {'visitors': vis, 'employees': emp, 'title': 'Employees', 'emp': '1', 'sos': '1'}
    template = 'users/roll_call.html'
    return render(request, template, parameters)


def export(request):
    """
    A function-based view for exporting the list of visitors for a specific date to a CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=visitors' + str(today) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'ID Number', 'Mobile Number', 'Email'])

    for visitor in vis_today:
        writer.writerow([visitor.vis_name, visitor.vis_id, visitor.vis_mob, visitor.vis_email])

    return response



## Messages
# messages.debug
# messages.info
# messages.success
# messages.warning
# messages.error
