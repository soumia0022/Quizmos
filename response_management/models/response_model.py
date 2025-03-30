from django.db import models
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll 
from django.conf import settings


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    poll = models.ForeignKey(Poll, on_delete=models.SET_NULL, null=True, default=1)
    submitted_on = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)
    session_code = models.IntegerField(default=0)

    class Meta:
        abstract = True

class MultipleChoiceResponse(Response):
    selected_options = models.JSONField()
    is_correct = models.BooleanField(default=False)

class SingleChoiceResponse(Response):
    selected_option = models.TextField()
    is_correct = models.BooleanField(default=False)

class TextFillResponse(Response):
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)

class DropdownFillResponse(Response):
    selected_option = models.TextField()
    is_correct = models.BooleanField(default=False)

class MatchQuestionResponse(Response):
    match_responses = models.JSONField()
    is_correct = models.BooleanField(default=False)

class WordCloudResponse(Response):
    word_cloud_response = models.JSONField(default=dict)
    is_correct = models.BooleanField(default=False)

class CodeQuestionResponse(Response):
    submitted_code = models.TextField()
    is_correct = models.BooleanField(default=False)