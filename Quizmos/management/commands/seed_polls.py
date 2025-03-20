from django.core.management.base import BaseCommand
from faker.providers import BaseProvider

from poll_management.models.poll_model import Poll
from user_management.models import User
from faker import Faker


class QuizTopicProvider(BaseProvider):
    def quiz_question(self):
        quiz_topics = [
            "Fundamentals of Programming",
            "Data Structures and Algorithms",
            "Object-Oriented Programming (OOP)",
            "Operating Systems Concepts",
            "Computer Networks",
            "Database Management Systems (DBMS)",
            "Cybersecurity Basics",
            "Web Development (HTML, CSS, JavaScript)",
            "Backend Development (Node.js, Django, Flask, etc.)",
            "Frontend Frameworks (React, Angular, Vue)",
            "Cloud Computing and Virtualization",
            "Software Development Life Cycle (SDLC)",
            "Machine Learning and Artificial Intelligence",
            "Version Control Systems (Git, GitHub)",
            "RESTful APIs and Web Services",
            "Big Data and Data Analytics",
            "Internet of Things (IoT)",
            "Blockchain Technology",
            "Programming Paradigms",
            "Computer Science History and Pioneers",
            "Linux and Command Line",
            "Mobile App Development (iOS, Android, Flutter, React Native)",
            "DevOps and CI/CD Pipelines",
            "Cybersecurity Attacks and Defense Mechanisms",
            "Cloud Platforms (AWS, Azure, Google Cloud)",
            "Programming Language Concepts",
            "Concurrency and Parallel Computing",
            "Computer Graphics and Game Development",
            "Embedded Systems and Robotics",
            "Artificial Neural Networks and Deep Learning"
        ]
        question = self.random_element(quiz_topics)

        return question

class Command(BaseCommand):
    """Build automation command to seed the database"""

    POLL_COUNT_PER_LECTURER = 3
    help = 'Seed the database with polls'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        self.faker.add_provider(QuizTopicProvider)

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
            title = self.faker.quiz_question(),
            user=lecturer,
        )