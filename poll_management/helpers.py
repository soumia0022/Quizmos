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
