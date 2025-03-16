from collections import Counter
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from poll_management.models.poll_model import Poll
from response_management.models.response_model import MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse, \
    DropdownFillResponse, MatchQuestionResponse, WordCloudResponse, CodeQuestionResponse
from question_management.models.question_models import Question

def poll_analytics(request, poll_id):
    """To do with analytics for the whole poll."""
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'poll_detail.html', {'poll': poll})


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

        # For each code response count
        # responses = CodeQuestionResponse.objects.filter(question=question)
        # code_snippets = [response.submitted_code for response in responses]
        # code_counts = Counter(code_snippets)
        # if code_counts:
        #     labels, data = zip(*code_counts.items())
        # else:
        #     labels = []
        #     data = []


    return JsonResponse({'question': question.question_text, 'labels': labels, 'data': data})
