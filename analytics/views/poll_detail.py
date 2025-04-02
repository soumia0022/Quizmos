# Needs refactoring

from collections import Counter

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from poll_management.models.poll_model import Poll
from response_management.models.response_model import MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse, \
    DropdownFillResponse, MatchQuestionResponse, WordCloudResponse, CodeQuestionResponse
from question_management.models.question_models import Question
from analytics.helpers import apply_search_and_sort
from django.db.models.functions import Lower
from user_management.helpers import role_required


@login_required
@role_required('Lecturer')
def poll_analytics(request, poll_id):
    """To do with analytics for the whole poll."""
    poll = get_object_or_404(Poll, id=poll_id)

    if poll.user != request.user:
        raise PermissionDenied("You do not have permission to access this poll's analytics") # Message in terminal

    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'question_text_asc')

    questions = poll.questions.all()

    sort_options = {
        'question_text_asc': Lower('question_text'),
        'question_text_desc': Lower('question_text').desc(),
        'type_asc': 'question_type',
        'type_desc': '-question_type'
    }

    questions = apply_search_and_sort(
        questions,
        search_query=search_query,
        sort_by=sort_by,
        sort_options=sort_options,
        default_sort='question_text'
    )

    return render(request, 'poll_detail.html', {
        'poll': poll,
        'questions': questions,
        'search_query': search_query,
        'sort_by': sort_by
    })


def get_response_count(poll, question):
    """Helper function to get response count for a question."""
    response_models = {
        'multiple_choice': MultipleChoiceResponse,
        'single_choice': SingleChoiceResponse,
        'text_fill': TextFillResponse,
        'dropdown_fill': DropdownFillResponse,
        'match_question': MatchQuestionResponse,
        'wordcloud': WordCloudResponse,
    }

    model = response_models.get(question.question_type)

    if model:
        return model.objects.filter(poll=poll, question=question).count()
    return 0


def get_graph_data(request, poll_id):
    """Extracts question text and response counts for each question."""
    poll = get_object_or_404(Poll, id=poll_id)
    questions = poll.questions.all()

    labels = [question.question_text for question in questions]
    data = [get_response_count(poll, question) for question in questions]

    return JsonResponse({'labels': labels, 'data': data})


def piechart_data(request, poll_id):
    return get_graph_data(request, poll_id)

def bargraph_data(request, poll_id):
    return get_graph_data(request, poll_id)

def linegraph_data(request, poll_id):
    return get_graph_data(request, poll_id)

def question_analytics(request, question_id):
    """Question-specific method to handle displaying of different question types."""
    question = get_object_or_404(Question.objects, id=question_id)
    labels = []
    data = []

    if question.question_type in ['multiple_choice', 'single_choice']:
        options = (
            question.multiple_choice_options
            if question.question_type == 'multiple_choice'
            else question.single_choice_option
        )

        response_model = MultipleChoiceResponse if question.question_type == 'multiple_choice' else SingleChoiceResponse
        responses = response_model.objects.filter(question=question)

        for option in options:
            count = sum(1 for response in responses if option in getattr(response, 'selected_options', '') or option in getattr(response, 'selected_option', ''))
            labels.append(option)
            data.append(count)

    elif question.question_type == 'text_fill':
        responses = TextFillResponse.objects.filter(question=question).values_list('answer_text', flat=True)
        response_counts = Counter(responses)
        labels, data = list(response_counts.keys()), list(response_counts.values())

    elif question.question_type == 'dropdown_fill':
        options = question.dropdown_options.split(',')
        for option in options:
            count = DropdownFillResponse.objects.filter(question=question, selected_option=option).count()
            labels.append(option)
            data.append(count)

    elif question.question_type == 'match_question':
        labels.append("Total Number of Matches")
        data.append(MatchQuestionResponse.objects.filter(question=question).count())

    elif question.question_type == 'wordcloud':
        responses = WordCloudResponse.objects.filter(question=question)
        words = []
        for response in responses:
            words.extend(response.word_cloud_response)  # List of words

        word_counts = Counter(words)
        if word_counts:
            labels, data = zip(*word_counts.items())  # Words and their respective counts
        else:
            labels = []
            data = []

    elif question.question_type == 'code_question':
        responses_count = (CodeQuestionResponse.objects.filter(question=question)).count()
        labels = ['Total Number of Code Submissions']
        data = [responses_count]

    return JsonResponse({'question': question.question_text, 'labels': labels, 'data': data})

def question_correct_analytics(request, question_id):
    """Calculate the number of correct and incorrect responses for a given question.
    Uses the is_correct field across all response models."""
    question = get_object_or_404(Question, id=question_id)

    # Mapping of question types to their corresponding response models
    response_models = {
        'multiple_choice': MultipleChoiceResponse,
        'single_choice': SingleChoiceResponse,
        'text_fill': TextFillResponse,
        'dropdown_fill': DropdownFillResponse,
        'match_question': MatchQuestionResponse,
        'wordcloud': WordCloudResponse,
        'code_question': CodeQuestionResponse
    }

    # Get the appropriate response model
    response_model = response_models.get(question.question_type)

    if not response_model:
        return JsonResponse({
            'question': question.question_text,
            'labels': ['No analytics available'],
            'data': [0]
        })

    # Count correct and incorrect responses
    total_responses = response_model.objects.filter(question=question).count()
    correct_responses = response_model.objects.filter(question=question, is_correct=True).count()
    incorrect_responses = total_responses - correct_responses

    labels = ['Correct Responses', 'Incorrect Responses']
    data = [correct_responses, incorrect_responses]

    return JsonResponse({
        'question': question.question_text,
        'labels': labels,
        'data': data
    })

def poll_correct_analytics(request, poll_id):
    """Calculate total correct and incorrect responses for an entire poll."""
    poll = get_object_or_404(Poll, id=poll_id)
    questions = poll.questions.all()

    # Combine responses from all response models
    response_models = [
        MultipleChoiceResponse,
        SingleChoiceResponse,
        TextFillResponse,
        DropdownFillResponse,
        MatchQuestionResponse,
        WordCloudResponse,
        CodeQuestionResponse
    ]

    total_correct = 0
    total_incorrect = 0

    for model in response_models:
        # Filter responses for this poll
        poll_responses = model.objects.filter(poll=poll)
        total_correct += poll_responses.filter(is_correct=True).count()
        total_incorrect += poll_responses.filter(is_correct=False).count()

    labels = ['Correct Responses', 'Incorrect Responses']
    data = [total_correct, total_incorrect]

    return JsonResponse({
        'labels': labels,
        'data': data
    })


def poll_correct_piechart_data(request, poll_id):
    return poll_correct_analytics(request, poll_id)

def poll_correct_bargraph_data(request, poll_id):
    return poll_correct_analytics(request, poll_id)
