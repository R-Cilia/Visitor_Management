from django.urls import path, include
from . import views
# from .views import VisitorInCreateView, VisitorOutCreateView

# The `urlpatterns` list routes URLs to views in the app.
urlpatterns = [
	# Home page for visitor and employee management
	path('', views.vis__emp, name='vm-vis__emp'),
	# Home page for visitor and employee management (manager access)
	path('manager/', views.vis__emp_manager, name='vm-vis__emp_manager'),

	# Visitors management
	# Page to list all visitors
	path('visitors/', views.visitors, name='vm-visitors'),
	# Page to manage visitors (manager access)
	path('visitors/manager/', views.visitor_manager, name='vm-vis_manager'),
	# Page to check-in visitors
	path('visitors/in/', views.visitor_in, name='vm-visIN'),
	# Page to search for visitors
	path('visitors/search/', views.visitor_search, name='vm-vis_search'),
	# Page to check-out visitors
	path('visitors/out/', views.visitor_out, name='vm-visOUT'),
	# Page to confirm visitor check-out
	path('visitors/out/<pk>/', views.vis_save_exit, name='vm-vis_confirmOUT'),

	# Employees management
	# Page to list all employees
	path('employees/', views.employees, name='vm-employees'),
	# Page to manage employees (manager access)
	path('employees/manager/', views.employee_manager, name='vm-emp_manager'),
	# Page to search for employees
	path('employees/search/', views.employee_search, name='vm-emp_search'),
	# Page to search for present employees
	path('employees/search/present/', views.present_employee_search, name='vm-present_emp_search'),
	# Page to check-in employees
	path('employees/in/', views.employee_in, name='vm-empIN'),
	# Page to check-out employees
	path('employees/out/', views.employee_out, name='vm-empOUT'),
	# Page to send SOS
	path('employees/sos/', views.sos, name='vm-sos'),
	# Page for roll call
	path('employees/sos/roll_call/', views.sos, name='vm-roll_call'),

	# Terms and conditions
	# Page to show terms and conditions
	path('terms/', views.terms, name='vm-terms'),
]
