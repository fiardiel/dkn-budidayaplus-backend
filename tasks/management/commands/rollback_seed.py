from django.core.management.base import BaseCommand
from django.db import transaction
from tasks.models import TaskTemplate

class Command(BaseCommand):
    help = 'Rollback all TaskTemplate data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting rollback of all TaskTemplate data...")

        try:
            with transaction.atomic():
                count = TaskTemplate.objects.count()

                TaskTemplate.objects.all().delete()

                self.stdout.write(self.style.SUCCESS(f"Successfully rolled back {count} TaskTemplate records."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error during rollback: {str(e)}"))
