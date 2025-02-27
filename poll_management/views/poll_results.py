from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from response_management.models.response_model import MatchQuestionResponse, MultipleChoiceResponse, SingleChoiceResponse, DropdownFillResponse, TextFillResponse, WordCloudResponse
import json

def poll_results(request, code):
    poll = get_object_or_404(Poll, number_code=code)

    return render(request, 'poll_results.html', {'poll': poll})
