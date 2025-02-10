from django.core.management.base import BaseCommand
from poll_management.models.poll_model import Poll
from user_management.models import User
from faker import Faker


class Command(BaseCommand):
    """Build automation command to seed the database"""

    POLL_COUNT_PER_LECTURER = 5
    help = 'Seed the database with polls'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_polls()
        self.polls = Poll.objects.all()

    def create_polls(self):
        """Create polls for each lecturer"""
        lecturers = list(User.objects.filter(role='Lecturer'))
        if not lecturers:
            print("No lecturers found. Please seed users first.")
            return

        lecturerCount = 0
        for lecturer in lecturers:
            lecturerCount += 1
            for i in range(self.POLL_COUNT_PER_LECTURER):
                self.generate_poll(lecturer)
                print(f"Created poll #{i} for lecturer #{lecturerCount}", end='\r')

        print(f"Seeded {self.POLL_COUNT_PER_LECTURER * len(lecturers)} polls.                                                     ")

    def generate_poll(self, lecturer):
        """Generate a single poll for lecturer"""
        Poll.objects.create(
            title = self.faker.catch_phrase(),
            user=lecturer,
        )