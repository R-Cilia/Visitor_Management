from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

# The Profile model represents the user profile for a given user.
# It has a one-to-one relationship with the built-in Django User model.
# It also has an image field for storing a profile picture.
class Profile(models.Model):
	# A one-to-one field to the built-in User model
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# An image field for storing a profile picture
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	# A string representation of the model
	def __str__(self):
		return f'{self.user.username} Profile'

# The Sos model represents a user's emergency contact information.
# It has a foreign key to the built-in Django User model to establish a relationship between a user and their emergency contact.
# It also has a boolean field for indicating whether the emergency contact is currently active or not.
class Sos(models.Model):
	# An email field for storing the emergency contact's email address
	sos_email = models.EmailField(blank=True, null=True)
	# A boolean field for indicating whether the emergency contact is currently active or not
	status = models.BooleanField(default=True)
	# A foreign key to the built-in User model to establish a relationship between a user and their emergency contact
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	# A string representation of the model
	def __str__(self):
		return f'{self.sos_email}'
