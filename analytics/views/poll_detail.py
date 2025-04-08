from collections import Counter
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models.functions import Lower

from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question
from response_management.models.response_model import (
    MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse,
    DropdownFillResponse, MatchQuestionResponse, WordCloudResponse, CodeQuestionResponse
)
from analytics.helpers import apply_search_and_sort
from user_management.helpers import role_required

def ajax_required(view_func):
    """To prevent direct URL access."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return HttpResponseForbidden("Access denied")
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
@role_required('Lecturer')
def poll_analytics(request, poll_id):
    """View to display analytics for the whole poll."""
    poll = get_object_or_404(Poll, id=poll_id)

    if poll.user != request.user:
        raise PermissionDenied("You do not have permission to access this poll's analytics")

    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'question_text_asc')

    sort_options = {
        'question_text_asc': Lower('question_text'),
        'question_text_desc': Lower('question_text').desc(),
        'type_asc': 'question_type',
        'type_desc': '-question_type'
    }

    questions = apply_search_and_sort(
        poll.questions.all(),
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
        'code_question': CodeQuestionResponse,
    }

    model = response_models.get(question.question_type)
    return model.objects.filter(poll=poll, question=question).count() if model else 0


@ajax_required
def poll_graph_data(request, poll_id, chart_type=None):
    """Generic method to extract question text and response counts for each question."""
    poll = get_object_or_404(Poll, id=poll_id)
    questions = poll.questions.all()

    labels = [question.question_text for question in questions]
    data = [get_response_count(poll, question) for question in questions]

    return JsonResponse({'labels': labels, 'data': data})


@ajax_required
def question_analytics(request, question_id):
    """Question-specific method to handle displaying of different question types."""
    question = get_object_or_404(Question.objects, id=question_id)
    labels, data = [], []

    if question.question_type in ['multiple_choice', 'single_choice']:
        labels, data = _process_choice_question(question)
    elif question.question_type == 'text_fill':
        labels, data = _process_text_fill_question(question)
    elif question.question_type == 'dropdown_fill':
        labels, data = _process_dropdown_question(question)
    elif question.question_type == 'match_question':
        labels = ["Total Number of Matches"]
        data = [MatchQuestionResponse.objects.filter(question=question).count()]
    elif question.question_type == 'wordcloud':
        labels, data = _process_wordcloud_question(question)
    elif question.question_type == 'code_question':
        labels = ['Total Number of Code Submissions']
        data = [CodeQuestionResponse.objects.filter(question=question).count()]

    return JsonResponse({'question': question.question_text, 'labels': labels, 'data': data})


def _process_choice_question(question):
    """Process multiple choice or single choice questions."""
    is_multiple = question.question_type == 'multiple_choice'
    options = question.multiple_choice_options if is_multiple else question.single_choice_option
    response_model = MultipleChoiceResponse if is_multiple else SingleChoiceResponse
    responses = response_model.objects.filter(question=question)

    labels, data = [], []
    for option in options:
        count = sum(1 for response in responses
                    if option in getattr(response, 'selected_options', '') or
                    option in getattr(response, 'selected_option', ''))
        labels.append(option)
        data.append(count)

    return labels, data


def _process_text_fill_question(question):
    """Process text fill questions."""
    responses = TextFillResponse.objects.filter(question=question).values_list('answer_text', flat=True)
    response_counts = Counter(responses)
    return list(response_counts.keys()), list(response_counts.values())


def _process_dropdown_question(question):
    """Process dropdown fill questions."""
    options = question.dropdown_options.split(',')
    labels, data = [], []
    for option in options:
        count = DropdownFillResponse.objects.filter(question=question, selected_option=option).count()
        labels.append(option)
        data.append(count)
    return labels, data


def _process_wordcloud_question(question):
    """Process wordcloud questions."""
    responses = WordCloudResponse.objects.filter(question=question)
    words = []
    for response in responses:
        words.extend(response.word_cloud_response)

    word_counts = Counter(words)
    if word_counts:
        return list(word_counts.keys()), list(word_counts.values())
    return [], []


RESPONSE_MODELS = {  # For correct/incorrect analytics
    'multiple_choice': MultipleChoiceResponse,
    'single_choice': SingleChoiceResponse,
    'text_fill': TextFillResponse,
    'dropdown_fill': DropdownFillResponse,
    'match_question': MatchQuestionResponse,
    'wordcloud': WordCloudResponse,
    'code_question': CodeQuestionResponse
}


@ajax_required
def question_correct_analytics(request, question_id):
    """Calculate the number of correct and incorrect responses for a given question."""
    question = get_object_or_404(Question, id=question_id)
    response_model = RESPONSE_MODELS.get(question.question_type)

    if not response_model:
        return JsonResponse({
            'question': question.question_text,
            'labels': ['No analytics available'],
            'data': [0]
        })

    total_responses = response_model.objects.filter(question=question).count()
    correct_responses = response_model.objects.filter(question=question, is_correct=True).count()
    incorrect_responses = total_responses - correct_responses

    return JsonResponse({
        'question': question.question_text,
        'labels': ['Correct Responses', 'Incorrect Responses'],
        'data': [correct_responses, incorrect_responses]
    })


@ajax_required
def poll_correct_analytics(request, poll_id, chart_type=None):
    """Calculate total correct and incorrect responses for an entire poll."""
    poll = get_object_or_404(Poll, id=poll_id)

    total_correct = 0
    total_incorrect = 0

    for model in RESPONSE_MODELS.values():
        poll_responses = model.objects.filter(poll=poll)
        total_correct += poll_responses.filter(is_correct=True).count()
        total_incorrect += poll_responses.filter(is_correct=False).count()

    return JsonResponse({
        'labels': ['Correct Responses', 'Incorrect Responses'],
        'data': [total_correct, total_incorrect]
    })