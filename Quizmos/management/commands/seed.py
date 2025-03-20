from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    """Build automation command to seed the database."""
    help = 'Seeds the database by running seed_users and seed_requests commands.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting the database seeding process...')

        # Run the seed_users command
        self.stdout.write('Seeding users...')
        call_command('seed_users')

        # Run the seed_requests command
        self.stdout.write('Seeding polls...')
        call_command('seed_polls')

        # Run the seed_bookings command
        self.stdout.write('Seeding questions...')
        call_command('seed_questions')

        self.stdout.write('Seeding responses...')
        call_command('seed_responses')

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!                                                        '))