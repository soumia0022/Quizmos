import json
import os
from django.conf import settings
from django.apps import apps
from user_management.models.user_model import User
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question


def load_default_responses():
    with open(os.path.join(settings.BASE_DIR, 'response_management/tests/fixtures/default_response.json'), 'r') as file:
        responses = json.load(file)

    for data in responses:
        model_label = data['model']  # e.g., "response_management.MultipleChoiceResponse"
        app_label, model_name = model_label.split('.')
        ModelClass = apps.get_model(app_label, model_name)

        fields = data['fields']
        user = User.objects.get(username=fields.pop('user'))
        poll = Poll.objects.get(pk=fields.pop('poll'))
        question = Question.objects.get(pk=fields.pop('question'))

        ModelClass.objects.get_or_create(
            pk=data['pk'],
            user=user,
            poll=poll,
            question=question,
            **fields
        )
