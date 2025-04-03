import csv

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from poll_management.models.poll_model import Poll
from response_management.models.response_model import MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse, DropdownFillResponse, MatchQuestionResponse
from user_management.helpers import role_required

@login_required
@role_required('Lecturer')
def download_csv(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if poll.user != request.user:
        raise PermissionDenied("You do not have permission to access this poll's analytics") # Message in terminal

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{poll.title}_responses.csv"'

    writer = csv.writer(response)
    writer.writerow(['User', 'Question', 'Question Type', 'Options', 'Correct Answer', 'Number of Responses'])

    for question in poll.questions.all():
        options = ""
        correct_answer = ""
        question_type = dict(question.QUESTION_TYPES).get(question.question_type, question.question_type)

        # Get responses based on question type
        if question.question_type == 'multiple_choice':
            options = ", ".join(question.multiple_choice_options)
            correct_answer = ", ".join(question.multiple_choice_answers)
            responses = MultipleChoiceResponse.objects.filter(question=question)
        elif question.question_type == 'single_choice':
            options = ", ".join(question.single_choice_option)
            correct_answer = ", ".join(question.single_choice_answers)
            responses = SingleChoiceResponse.objects.filter(question=question)
        elif question.question_type == 'text_fill':
            correct_answer = question.text_fill_answer
            responses = TextFillResponse.objects.filter(question=question)
        elif question.question_type == 'dropdown_fill':
            options = ", ".join(question.dropdown_options.split(','))
            correct_answer = question.dropdown_correct_answer
            responses = DropdownFillResponse.objects.filter(question=question)
        elif question.question_type == 'match_question':
            options = " | ".join([f"{q} -> {a}" for q, a in zip(question.match_options, question.match_answers)])
            correct_answer = options
            responses = MatchQuestionResponse.objects.filter(question=question)
        else:
            responses = MatchQuestionResponse.objects.none()  # Set empty QuerySet instead of list

        response_count = responses.count()

        for response_obj in responses:
            writer.writerow([
                response_obj.user.username if response_obj.user else "Anonymous",
                question.question_text,
                question_type,
                options,
                correct_answer,
                response_count
            ])

    return response
