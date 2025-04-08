from django.core.management.base import BaseCommand
from user_management.models import User

class Command(BaseCommand):
    """Command to delete all users from the database"""

    help = 'Delete all users from the database'

    def handle(self, *args, **options):
        deleted_count, _ = User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {deleted_count} users."))
