from django.core.management.base import BaseCommand
from visitor_management.models import Visitor


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        visitors = Visitor.objects.all()

        for visitor in visitors:
            visitor.delete()
            self.stdout.write(self.style.SUCCESS(f'{visitor.vis_name} has been wiped from the server!'))
