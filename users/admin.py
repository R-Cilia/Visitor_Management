from django.contrib import admin
from .models import Profile, Sos

# Import the Profile and Sos models from the current directory (.)

admin.site.register(Profile)
# Register the Profile model with the Django admin interface

admin.site.register(Sos)
# Register the Sos model with the Django admin interface
