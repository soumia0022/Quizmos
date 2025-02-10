from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    """Build automation command to seed the database."""
    help = 'Seeds the database by running seed_users and seed_requests commands.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting the database unseeding process...')

        # Run the seed_users command
        self.stdout.write('Unseeding users...')
        call_command('unseed_users')

        # Run the seed_requests command
        self.stdout.write('Unseeding polls...')
        call_command('unseed_polls')

        # Run the seed_bookings command
        self.stdout.write('Unseeding questions...')
        call_command('unseed_questions')

        self.stdout.write(self.style.SUCCESS('Database unseeding completed successfully!'))