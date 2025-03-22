from poll_management.helpers import format_youtube_link
from response_management.models.response_model import MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse, DropdownFillResponse, MatchQuestionResponse, CodeQuestionResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from poll_management.models.poll_model import Poll
from response_management.models.response_model import WordCloudResponse


@login_required
def student_view_poll(request, poll_id):
    """
    View function to display a student's poll responses.
    Args:
        request: The HTTP request object
        poll_id: The ID of the poll to view
    Returns:
        Rendered template with poll and response data
    """
    poll = get_object_or_404(Poll, id=poll_id)
    student = request.user


    response_types = {
        'multiple_choice': {'model': MultipleChoiceResponse,'value_field': 'selected_options'},
        'single_choice': {'model': SingleChoiceResponse,'value_field': 'selected_option'},
        'text_fill': {'model': TextFillResponse,'value_field': 'answer_text'},
        'dropdown': {'model': DropdownFillResponse,'value_field': 'selected_option'},
        'match': {'model': MatchQuestionResponse,'value_field': 'match_responses'},
        'code': {'model': CodeQuestionResponse,'value_field': 'submitted_code'},
        'word_cloud': {'model': WordCloudResponse, 'value_field': 'word_cloud_response'},
    }

    responses_by_question = {}

    for response_type, config in response_types.items():
        responses = config['model'].objects.filter(
            user=student,
            poll=poll
        ).select_related('question')

        # Process each response
        for response in responses:
            question = response.question

            if question.youtube_link:
                question.youtube_link = format_youtube_link(question.youtube_link)

            responses_by_question[question.id] = {
                'type': response_type,
                'question': question,
                'submitted_on': response.submitted_on
            }

            value_field = config['value_field']
            responses_by_question[question.id][value_field] = getattr(response, value_field)

            # print(f"Question ID: {question.id}, Response Type: {response_type}, Answer: {getattr(response, value_field, 'No Answer Found')}")

    return render(request, 'student_view_response/poll_response.html', {
        'poll': poll,
        'responses_by_question': responses_by_question
    })