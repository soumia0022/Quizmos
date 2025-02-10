import os
import matplotlib
from collections import Counter
from django.http import JsonResponse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import ImageFont
import base64
import io

def get_timer(request):
    """Use and validate the timer for each question."""
    timer = request.POST.get('question_timer')
    if not timer:
        return None
    try:
        return int(timer)
    except ValueError:
        return None

def generate_wordcloud_image(text, font_path):
    """Generate a wordcloud with pre-given text."""
    word_frequencies = Counter(text.split())

    if not os.path.exists(font_path):
        raise FileNotFoundError("Font file not found")
    try:
        font = ImageFont.truetype(font_path)
    except IOError:
        raise ValueError("Only supported for TrueType fonts")

    matplotlib.use('Agg')
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='twilight',
        max_font_size=100,
        min_font_size=10,
        font_path=font_path
    ).generate_from_frequencies(word_frequencies)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return base64.b64encode(buffer.getvalue()).decode()

def validate_question_options_and_answers(options, answers, question_type):
    """Validation for choice and matching questions."""
    if not options:
        return JsonResponse({'error': f'At least one option is required for a {question_type} question.'}, status=400)
    if not answers:
        return JsonResponse({'error': f'At least one answer is required for a {question_type} question.'}, status=400)
    return None