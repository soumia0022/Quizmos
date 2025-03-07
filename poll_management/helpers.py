from better_profanity import profanity
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
        if isinstance(response_data, str):
            text_data_json['response_data'] = profanity.censor(response_data)

        elif isinstance(response_data, list):
            text_data_json['response_data'] = [
                profanity.censor(item) if isinstance(item, str) else item
                for item in response_data
            ]

        elif isinstance(response_data, dict):
            for key, value in response_data.items():
                if isinstance(value, str):
                    response_data[key] = profanity.censor(value)
        return text_data_json

