import json
import os
from django.conf import settings
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question


def load_default_questions():
    with open(os.path.join(settings.BASE_DIR, 'question_management/tests/fixtures/default_question.json'), 'r') as file:
        questions = json.load(file)

    for data in questions:
        fields = data['fields']
        poll = Poll.objects.get(pk=fields.pop('poll'))
        Question.objects.get_or_create(pk=data['pk'], poll=poll, **fields)
