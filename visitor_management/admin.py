from django.contrib import admin
from .models import Visitor, Employee

# Register Visitor and Employee Models in the admin interface

admin.site.register(Visitor)
admin.site.register(Employee)
