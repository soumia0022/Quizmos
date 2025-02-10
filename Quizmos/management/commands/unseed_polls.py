from django.core.management.base import BaseCommand
from poll_management.models.poll_model import Poll

class Command(BaseCommand):
    """Command to unseed (delete) all poll data."""

    help = "Deletes all seeded polls"

    def handle(self, *args, **options):
        poll_count = Poll.objects.count()
        if poll_count == 0:
            self.stdout.write(self.style.WARNING("No polls found to delete."))
            return

        Poll.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {poll_count} polls."))
