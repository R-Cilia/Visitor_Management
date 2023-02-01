import django_filters
from .models import *

## VisitorFilter class for filtering visitor records based on different criteria
class VisitorFilter(django_filters.FilterSet):
    ## Meta class to define the filter fields
	class Meta:
		## Define the model to be used for filtering
		model = Visitor
		## Define the fields that can be used for filtering
		fields = '__all__'
		## To limit the fields, the following can be used
		# fields = {
		# 	'vis_name': ['icontains'],
		# }
