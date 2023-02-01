from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Sos

# 'UserRegisterForm' is a form for creating a new user account
# It extends the built-in 'UserCreationForm' and adds an 'email' field

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField() # define the email field as an 'EmailField'

	# Inner Meta class to specify additional information about the form
	class Meta:
		# Specify that the form will be working with the 'User' model
		model = User
		# Specify the fields that will be included in the form, in the order they should appear
		fields = ['username', 'email', 'password1', 'password2']


# 'UserUpdateForm' is a form for updating an existing user's account information
# It allows the user to update their 'username' and 'email' fields

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField() # define the email field as an 'EmailField'

	# Inner Meta class to specify additional information about the form
	class Meta:
		# Specify that the form will be working with the 'User' model
		model = User
		# Specify the fields that will be included in the form, in the order they should appear
		fields = ['username', 'email']



# 'SosForm' is a form for creating or updating a 'Sos' model instance
# It allows the user to specify an 'sos_email' and a 'status'

class SosForm(forms.ModelForm):
	# Inner Meta class to specify additional information about the form
	class Meta:
	# Specify that the form will be working with the 'Sos' model
	model = Sos
	# Specify the fields that will be included in the form, in the order they should appear
	fields = ['sos_email', 'status']
