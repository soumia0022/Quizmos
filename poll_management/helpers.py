from better_profanity import profanity
from django.conf import settings
import uuid
import os

def format_youtube_link(link):
    """
    Format YouTube links for proper embedding.
    Args:
        link: The original YouTube link
    Returns:
        Properly formatted embed URL
    """
    if 'youtu.be/' in link:
        return link.replace("youtu.be/", "www.youtube.com/embed/")
    elif 'youtube.com/watch?v=' in link:
        return link.replace("youtube.com/watch?v=", "youtube.com/embed/")
    elif 'youtube.com/embed/' not in link:
        # Handle other potential YouTube URL formats
        import re
        video_id = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', link)
        if video_id:
            return f"https://www.youtube.com/embed/{video_id.group(1)}"
    return link

def apply_profanity_filter(text_data_json, message_type):
    """
    Apply profanity filter to responses.
    """

    if message_type == 'response' and 'response_data' in text_data_json:
        response_data = text_data_json.get('response_data')
        response_type = text_data_json.get('response_type')

        if isinstance(response_data, str):
            text_data_json['response_data'] = profanity.censor(response_data)

        elif isinstance(response_data, list):
            filtered_list = []

            if response_type == 'match_question':
                for item in response_data:
                    if isinstance(item, dict):
                        filtered_item = {}
                        for key, value in item.items():
                            if isinstance(value, str):
                                filtered_item[key] = profanity.censor(value)
                            else:
                                filtered_item[key] = value
                        filtered_list.append(filtered_item)
                    elif isinstance(item, str):
                        filtered_list.append(profanity.censor(item))
                    else:
                        filtered_list.append(item)
            else:
                for item in response_data:
                    if isinstance(item, str):
                        filtered_list.append(profanity.censor(item))
                    else:
                        filtered_list.append(item)

            text_data_json['response_data'] = filtered_list

        elif isinstance(response_data, dict):
            for key, value in response_data.items():
                if isinstance(value, str):
                    response_data[key] = profanity.censor(value)
        return text_data_json


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

