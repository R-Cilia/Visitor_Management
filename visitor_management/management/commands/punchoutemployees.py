from django.core.management.base import BaseCommand
from visitor_management.models import Employee


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        employees = Employee.objects.all()

        for employee in employees:
            if employee.status == True:
                employee.status = False
                employee.save()
                self.stdout.write(self.style.SUCCESS(f'{employee.emp_name} has been punched out!'))
            else:
                pass
