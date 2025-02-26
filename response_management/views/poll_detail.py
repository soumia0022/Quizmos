from django.shortcuts import get_object_or_404, render
from poll_management.models.poll_model import Poll
from response_management.models.response_model import MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse, DropdownFillResponse, MatchQuestionResponse
from django.http import HttpResponse, JsonResponse
import csv


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'poll_detail.html', {'poll': poll})

def piechart_data(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    # Get the questions for the poll
    questions = poll.questions.all()

    # Initialize the data
    labels = []
    data = []

    for question in questions:
        # For each question, count the number of responses
        response_count = 0
        if question.question_type == 'multiple_choice':
            response_count = MultipleChoiceResponse.objects.filter(poll=poll, question=question).count()
        elif question.question_type == 'single_choice':
            response_count = SingleChoiceResponse.objects.filter(poll=poll, question=question).count()
        elif question.question_type == 'text_fill':
            response_count = TextFillResponse.objects.filter(poll=poll, question=question).count()
        elif question.question_type == 'dropdown_fill':
            response_count = DropdownFillResponse.objects.filter(poll=poll, question=question).count()
        elif question.question_type == 'match_question':
            response_count = MatchQuestionResponse.objects.filter(poll=poll, question=question).count()

        labels.append(question.question_text)  # Label is the question text
        data.append(response_count)  # Data is the response count

    # Return the data as JSON
    return JsonResponse({'labels': labels, 'data': data})

# views.py
def bargraph_data(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    questions = poll.questions.all()

    labels = []
    data = []

    for question in questions:
        response_count = 0
        if question.question_type == 'multiple_choice':
            response_count = MultipleChoiceResponse.objects.filter(poll=poll, question=question).count()
        elif question.question_type == 'single_choice':
            response_count = SingleChoiceResponse.objects.filter(poll=poll, question=question).count()
        elif question.question_type == 'text_fill':
            response_count = TextFillResponse.objects.filter(poll=poll, question=question).count()
        elif question.question_type == 'dropdown_fill':
            response_count = DropdownFillResponse.objects.filter(poll=poll, question=question).count()
        elif question.question_type == 'match_question':
            response_count = MatchQuestionResponse.objects.filter(poll=poll, question=question).count()

        labels.append(question.question_text)
        data.append(response_count)

    return JsonResponse({'labels': labels, 'data': data})


def linegraph_data(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    questions = poll.questions.all()

    labels = []
    data = []

    for question in questions:
        response_count = 0
        if question.question_type == 'multiple_choice':
            response_count = MultipleChoiceResponse.objects.filter(poll=poll, question=question).count()
        elif question.question_type == 'single_choice':
            response_count = SingleChoiceResponse.objects.filter(poll=poll, question=question).count()
        elif question.question_type == 'text_fill':
            response_count = TextFillResponse.objects.filter(poll=poll, question=question).count()
        elif question.question_type == 'dropdown_fill':
            response_count = DropdownFillResponse.objects.filter(poll=poll, question=question).count()
        elif question.question_type == 'match_question':
            response_count = MatchQuestionResponse.objects.filter(poll=poll, question=question).count()

        labels.append(question.question_text)
        data.append(response_count)

    return JsonResponse({'labels': labels, 'data': data})
