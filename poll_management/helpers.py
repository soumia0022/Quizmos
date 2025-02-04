from django.conf import settings
import os
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

def generate_number_code():
    return str(uuid.uuid4().int)[:6]