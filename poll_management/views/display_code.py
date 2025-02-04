import json
import qrcode
import uuid
import os
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from poll_management.models.poll_model import Poll
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime
from poll_management.helpers import generate_number_code, delete_old_qr_codes


def display_code(request, pk):
    # Get the poll and set it to active
    poll = get_object_or_404(Poll, pk=pk)
    poll.status = 'active'
    poll.save()

    # Clean up old QR codes
    delete_old_qr_codes(poll)

    # Generate unique codes
    unique_id = str(uuid.uuid4())[:8]
    poll.number_code = generate_number_code()
    poll.save()

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Generate join URL and QR code
    join_url = f"{request.scheme}://{request.get_host()}/polls/join/{poll.number_code}/"
    qr.add_data(join_url)
    qr.make(fit=True)

    # Create and save QR code image
    img = qr.make_image(fill_color="#003366", back_color="white")
    filename = f"qr_code_{poll.title}_{poll.pk}_{unique_id}.png"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    img.save(filepath)

    qr_url = os.path.join(settings.MEDIA_URL, filename)

    # Prepare questions data for JSON
    questions_data = []
    for question in poll.questions.all():
        question_dict = {
            'id': str(question.id),
            'type': question.question_type,
            'text': '',
            'options': [],
            'created_at': question.created_at.isoformat() if hasattr(question, 'created_at') else None
        }

        # Set question-specific data based on type
        if question.question_type == 'dropdown_fill':
            question_dict.update({
                'text': question.dropdown_fill_question,
                'options': question.get_dropdown_options()
            })
        elif question.question_type == 'text_fill':
            question_dict.update({
                'text': question.text_fill_question
            })
        elif question.question_type == 'multiple_choice':
            question_dict.update({
                'text': question.multiple_choice_question,
                'options': question.multiple_choice_options
            })
        elif question.question_type == 'single_choice':
            question_dict.update({
                'text': question.single_choice_question,
                'options': question.single_choice_option
            })
        elif question.question_type == 'wordcloud':
            question_dict.update({
                'text': question.wordcloud_question
            })
        elif question.question_type == 'match_question':
            question_dict.update({
                'text': question.match_question,
                'options': question.match_options,
                'answers': question.match_answers
            })

        questions_data.append(question_dict)

    # Send WebSocket message about poll activation
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'poll_{poll.number_code}',
        {
            'type': 'poll_message',
            'message': f'Poll activated: {poll.title}',
            'timestamp': datetime.now().isoformat()
        }
    )

    # Prepare context data for template
    context = {
        'poll': poll,
        'code': poll.number_code,
        'qrcode': qr_url,
        'questions_json': json.dumps(questions_data),
        'join_url': join_url,
        'host': request.get_host(),
    }

    return render(request, 'display_code.html', context)