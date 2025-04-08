from poll_management.helpers import format_youtube_link
from response_management.models.response_model import (
    MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse,
    DropdownFillResponse, MatchQuestionResponse, WordCloudResponse,
    CodeQuestionResponse
)
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from poll_management.models.poll_model import Poll


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
    # Get the poll
    poll = get_object_or_404(Poll, id=poll_id)
    student = request.user
    session_code = request.GET.get('session_code')

    # Collect all unique session codes for this poll and student
    response_types = [
        MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse,
        DropdownFillResponse, MatchQuestionResponse, WordCloudResponse,
        CodeQuestionResponse
    ]

    session_codes = set()
    responses_by_question = {}

    response_type_config = {
        MultipleChoiceResponse: {'value_field': 'selected_options'},
        SingleChoiceResponse: {'value_field': 'selected_option'},
        TextFillResponse: {'value_field': 'answer_text'},
        DropdownFillResponse: {'value_field': 'selected_option'},
        MatchQuestionResponse: {'value_field': 'match_responses'},
        WordCloudResponse: {'value_field': 'word_cloud_response'},
        CodeQuestionResponse: {'value_field': 'submitted_code'}
    }

    for response_type in response_types:
        filter_kwargs = {
            'user': student,
            'poll': poll
        }
        if session_code:
            filter_kwargs['session_code'] = session_code

        responses = response_type.objects.filter(**filter_kwargs).select_related('question')

        session_codes.update(responses.values_list('session_code', flat=True))

        for response in responses:
            question = response.question

            if question.youtube_link:
                question.youtube_link = format_youtube_link(question.youtube_link)

            config = response_type_config.get(type(response), {})

            # Get correctness
            is_correct = response.is_correct
            value_field = config['value_field']
            student_answer = getattr(response, value_field)

            response_data = {
                'type': response_type.__name__.lower().replace('response', ''),
                'question': question,
                'submitted_on': response.submitted_on,
                'is_correct': is_correct,
                value_field: student_answer,
                'session_code': response.session_code,
            }


            if response_type in [MultipleChoiceResponse, MatchQuestionResponse]:
                response_data['is_partially_correct'] = getattr(response, 'is_partially_correct', False)

            responses_by_question[question.id] = response_data

    return render(request, 'student_view_response/poll_response.html', {
        'poll': poll,
        'responses_by_question': responses_by_question,
        'session_codes': list(session_codes),
        'selected_session_code': session_code
    })