from django.http import HttpResponseForbidden
from django.shortcuts import  render, get_object_or_404
from django.urls import reverse

from poll_management.models.poll_model import Poll
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import uuid
import qrcode
import os

#move these to helpers.py--------
def ensure_media_directory_exists():
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

def delete_old_qr_codes(poll):
    """Delete old QR code images for a specific poll"""
    ensure_media_directory_exists() 
    for filename in os.listdir(settings.MEDIA_ROOT):
        if filename.startswith(f"qr_code_{poll.title}_{poll.pk}_"):
            os.remove(os.path.join(settings.MEDIA_ROOT, filename))

def generate_number_code():
    return str(uuid.uuid4().int)[:6]
#------------------------------------
def display_code(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    if poll.questions.count() == 0:
        return HttpResponseForbidden("This poll has no questions and cannot be started.")

    poll.status = 'active'
    poll.save()
    delete_old_qr_codes(poll)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Add the poll's title, primary key, and the unique number code to the QR code data
    unique_id = str(uuid.uuid4())[:8]
    poll.number_code = generate_number_code()
    poll.save()
    relative_url = reverse('poll_management:join_poll', kwargs={'code': poll.number_code})

    join_url = request.build_absolute_uri(relative_url)
    qr.add_data(join_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#003366", back_color="white")
    filename = f"qr_code_{poll.title}_{poll.pk}_{unique_id}.png"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    img.save(filepath)
    
    qr_url = os.path.join(settings.MEDIA_URL, filename)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'poll_{poll.number_code}',
        {
            'type': 'poll_message',
            'message': f'A student joined the poll: {poll.title}!'
        }
    )#
    return render(request, 'display_code.html', {'poll': poll, 'code': poll.number_code, 'qrcode': qr_url})
