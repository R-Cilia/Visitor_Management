from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
import datetime

from django.contrib.auth.models import User

## Employee Model
class Employee(models.Model):
	# Automatically generated ID field for each instance of Employee model
	id = models.AutoField

	# Foreign key field that references to the User model.
	# On deletion of related user, all the related employees will be deleted as well.
	admin = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

	# CharField for storing employee name with max length of 60 characters
	emp_name = models.CharField(max_length=60, default='')

	# CharField for storing employee ID with max length of 15 characters
	emp_id = models.CharField(max_length=15, default='')

	# EmailField for storing employee email address
	emp_email = models.EmailField(blank=True, null=True)

	# CharField for storing employee mobile number with max length of 15 characters
	emp_mob = models.CharField(max_length=15, default='')

	# DateField for storing the date when this record was created
	date = models.DateField(default=timezone.localdate())

	# BooleanField for storing the current status of the employee
	status = models.BooleanField(default=False)

	# BooleanField for checking if the terms and conditions are accepted
	check = models.BooleanField(default=False)

	# SlugField for storing a unique identifier for each instance of Employee model
	# It will be constructed by combining the primary key, name and ID of the employee
	slug = models.SlugField(max_length=75, default='', blank=True)

	def __str__(self):
		# Returns a string representation of this instance
		return (str(self.id) + ':: ' + self.emp_name + '; ' + self.emp_id)

	def save(self, *args, **kwargs):
		# Overriding the save method to add custom functionality
		# The functionality to switch the status of the employee has been commented out
		#
		# if self.status == False:
		# 	self.status = True
		# elif self.status == True:
		# 	self.status = False

		# Creating the unique identifier for each instance of Employee model
		self.slug = slugify( 'pk=' + str(self.id) + '&name=' + self.emp_name + '&id=' + self.emp_id)

		# Calling the parent's save method to save the instance
		super(Employee, self).save(*args, **kwargs)

	def get_absolute_url(self):
		# Returns the URL for detail view of this instance
		return reverse("use-dashboard_detail", kwargs={'pk': self.pk})



## Visitor Model
class Visitor(models.Model):
    # AutoField for primary key of the model
    id = models.AutoField()

    # ForeignKey to the User model to connect the visitor with an admin who registered them
    admin = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    # CharField to store the visitor's name, max length is 60 characters
    vis_name = models.CharField(max_length=60, default='')

    # ForeignKey to the Employee model to store who the visitor is visiting
    visiting = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    # CharField to store the visitor's identification number, max length is 15 characters
    vis_id = models.CharField(max_length=15, default='')

    # EmailField to store the visitor's email address
    vis_email = models.EmailField(blank=True, null=True)

    # CharField to store the visitor's mobile number, max length is 15 characters
    vis_mob = models.CharField(max_length=15, default='')

    # DateField to store the date of visit, default is the current local date
    date = models.DateField(default=timezone.localdate())

    # BooleanField to store the check-in status of the visitor
    status = models.BooleanField(default=False)
    
    # BooleanField to store whether the visitor has agreed to the terms and conditions
    check = models.BooleanField(default=False)

    # SlugField to store a unique identifier for the visitor, generated using the visitor's name and id
    slug = models.SlugField(max_length=75, default='', blank=True)

    # Method to return the string representation of the model
    def __str__(self):
        return (str(self.id) + ':: ' + self.vis_name + '; ' + self.vis_id)

    # Method to save the model, generates a unique slug for the visitor
    def save(self, *args, **kwargs):
        self.slug = slugify( 'pk=' + str(self.id) + '&name=' + self.vis_name + '&id=' + self.vis_id)
        super(Visitor, self).save(*args, **kwargs)
