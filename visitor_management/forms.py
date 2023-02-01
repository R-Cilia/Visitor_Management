from django import forms
from .models import Visitor, Employee


## Add a visitor form
class VisitorForm(forms.ModelForm):
    # CharField to represent visiting information of the visitor
    visiting = forms.CharField(required=False)

    # BooleanField to represent the check-in/check-out status of the visitor
    check = forms.BooleanField(required=True)

    class Meta:
        # Define the model to be used by the form
        model = Visitor

        # Define the fields to be displayed in the form,
        # including the fields from the Visitor model
        fields = ('id', 'vis_name', 'vis_id', 'vis_email', 'vis_mob',
                  'check', 'status', 'date', 'visiting')

        # Define the initial value for the `status` field
        def __init__(self, *args, **kwargs):
            super(VisitorForm, self).__init__(*args, **kwargs)
            self.initial['status'] = True



## Add a employee form
class EmployeePunchingForm(forms.ModelForm):
    """
    A form for punching in/out of employees.

    Attributes:
        status (BooleanField): A boolean field to represent whether an employee is punching in or out.
    """
    status = forms.BooleanField(required=True)

    class Meta:
        """
        Meta class to specify the model and fields used in the form.
        """
        model = Employee
        fields = ('emp_name', 'emp_id', 'status')
