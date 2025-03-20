from django.core.management.base import BaseCommand
from response_management.models.response_model import (
    MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse,
    DropdownFillResponse, MatchQuestionResponse, WordCloudResponse,
    CodeQuestionResponse
)


class Command(BaseCommand):
    help = 'Delete all seeded responses from the database'

    def handle(self, *args, **kwargs):
        response_models = [
            MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse,
            DropdownFillResponse, MatchQuestionResponse, WordCloudResponse,
            CodeQuestionResponse
        ]

        total_deleted = 0
        for model in response_models:
            deleted_count, _ = model.objects.all().delete()
            total_deleted += deleted_count

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {total_deleted} responses'))
