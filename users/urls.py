from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_views
from .views import (
    DashboardListView,  # class-based view for list of Employees
    DashboardDetailView,  # class-based view for detail view of a specific Employee
    DashboardCreateView,  # class-based view for creating a new Employee
    DashboardUpdateView,  # class-based view for updating an existing Employee
    DashboardDeleteView,  # class-based view for deleting an existing Employee
    DashboardVisitorListView,  # class-based view for list of Visitors
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', user_views.home, name='use-home'),  # Redirects to login page
    path('register/', user_views.register, name="use-register"),  # View for user registration

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="use-login"),  # View for user login
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="use-logout"),  # View for user logout
    path('dashboard/', user_views.dashboard, name='use-dashboard'),  # View for dashboard

    path('dashboard/visitors/', DashboardVisitorListView.as_view(), name='use-dashboard_visitors'),  # View for list of Visitors
    path('dashboard/visitors/export/', user_views.export, name='use-dashboard_visitors_export'),  # View for exporting list of Visitors as a CSV file

    path('dashboard/employee', DashboardListView.as_view(), name='use-dashboard_employees'),  # View for list of Employees
    path('dashboard/employee/<int:pk>/', DashboardDetailView.as_view(), name="use-dashboard_detail"),  # View for detail view of a specific Employee
    path('dashboard/employee/new/', DashboardCreateView.as_view(), name="use-dashboard_create"),  # View for creating a new Employee
    path('dashboard/employee/<int:pk>/update/', DashboardUpdateView.as_view(), name="use-dashboard_update"),  # View for updating an existing Employee
    path('dashboard/employee/<int:pk>/delete/', DashboardDeleteView.as_view(), name="use-dashboard_delete"),  # View for deleting an existing Employee

    path('dashboard/roll_call/', user_views.roll_call, name='use__roll_call'),  # View for roll call
    path('profile/', user_views.profile, name="use-profile"),  # View for user profile page
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
