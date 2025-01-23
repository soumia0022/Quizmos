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
import qrcode
import cv2
import numpy as np
from pyzbar.pyzbar import decode

def extract_number_from_qr(qr_image_path):
    # Read the QR code image
    image = cv2.imread(qr_image_path)
    
    # Decode the QR code
    decoded_objects = decode(image)
    
    if decoded_objects:
        # Get the data from the first decoded object
        qr_data = decoded_objects[0].data.decode('utf-8')
        
        # Split the data and extract the number code
        # Assuming format: "poll_title-poll_pk-number_code-timestamp"
        parts = qr_data.split('-')
        if len(parts) >= 3:
            return parts[2]  # The number code
    
    return None

def delete_old_qr_codes(poll):
    """Delete old QR code images for a specific poll"""
    for filename in os.listdir(settings.MEDIA_ROOT):
        if filename.startswith(f"qr_code_{poll.title}_{poll.pk}_"):
            os.remove(os.path.join(settings.MEDIA_ROOT, filename))

def display_code(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    poll.status = 'active'
    poll.save()


    # Delete old QR codes for this poll
    delete_old_qr_codes(poll)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Add the poll's title, primary key, and the unique number code to the QR code data
    unique_id = str(uuid.uuid4())[:8]
    qr.add_data(f"{poll.title}-{poll.pk}-{unique_id}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="#003366", back_color="white")
    filename = f"qr_code_{poll.title}_{poll.pk}_{unique_id}.png"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    img.save(filepath)
    extracted_number_code = extract_number_from_qr(filepath)
    
    qr_url = os.path.join(settings.MEDIA_URL, filename)

    return render(request, 'display_code.html', {'poll': poll, 'code': extracted_number_code, 'qrcode': qr_url})
