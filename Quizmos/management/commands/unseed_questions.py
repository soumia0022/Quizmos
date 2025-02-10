from django.core.management.base import BaseCommand
from question_management.models.question_models import Question

class Command(BaseCommand):
    """Command to delete all questions from the database"""

    help = 'Delete all questions from the database'

    def handle(self, *args, **options):
        deleted_count, _ = Question.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {deleted_count} questions."))
