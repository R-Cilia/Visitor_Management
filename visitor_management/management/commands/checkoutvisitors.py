from django.core.management.base import BaseCommand
from django.utils import timezone
from visitor_management.models import Visitor


today = timezone.localdate()


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        visitors = Visitor.objects.all().filter(date=today)

        for visitor in visitors:
            visitor.status = False
            visitor.save()
            self.stdout.write(self.style.SUCCESS(f'{visitor.vis_name} has been checked out!'))
