# polls/management/commands/cleanup_guests.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Cleanup guest users older than specified days'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete guest users created more than 1 day ago
        cutoff = timezone.now() - timedelta(days=1)
        deleted = User.objects.filter(
            username__startswith='guest_',
            date_joined__lt=cutoff
        ).delete()
        self.stdout.write(f'Deleted {deleted[0]} guest users')