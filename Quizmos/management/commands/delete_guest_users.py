from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.apps import apps

User = get_user_model()


class Command(BaseCommand):
    help = 'Deletes guest users that are older than one day'

    def handle(self, *args, **options):
        # calculate the cutoff time (24 hours ago)
        cutoff_time = timezone.now() - timedelta(days=1)
        guest_users = User.objects.filter(
            first_name='Guest',
            last_name='Guest',
            date_joined__lt=cutoff_time
        )

        count = guest_users.count()

        if count > 0:
            self.stdout.write(f'Found {count} guest users to delete...')


            # delete the guest users
            guest_users.delete()

            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {count} guest users')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('No guest users to delete')
            )