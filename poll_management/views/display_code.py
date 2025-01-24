from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
import qrcode
from io import BytesIO
import random
import os
import time
from poll_management.models.poll_model import Poll
from django.conf import settings
import uuid

def ensure_media_directory_exists():
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

def delete_old_qr_codes(poll):
    """Delete old QR code images for a specific poll"""
    ensure_media_directory_exists() 
    for filename in os.listdir(settings.MEDIA_ROOT):
        if filename.startswith(f"qr_code_{poll.title}_{poll.pk}_"):
            os.remove(os.path.join(settings.MEDIA_ROOT, filename))

def display_code(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
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
    number_code = str(random.randint(100000, 999999))
    qr.add_data(f"{poll.title}-{poll.pk}-{unique_id}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="#003366", back_color="white")
    filename = f"qr_code_{poll.title}_{poll.pk}_{unique_id}.png"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    img.save(filepath)
   
    
    qr_url = os.path.join(settings.MEDIA_URL, filename)

    return render(request, 'display_code.html', {'poll': poll, 'code': number_code, 'qrcode': qr_url})
