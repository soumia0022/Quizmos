import os
import json

import matplotlib
from django.http import JsonResponse
from question_management.models.question_models import Question
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import ImageFont
import base64
import io
from django.core.exceptions import ValidationError

def get_timer(request):
    timer = request.POST.get('question_timer')
    if not timer:
        return None
    try:
        return int(timer)
    except ValueError:
        return None

def save_files(request, question):
    if 'audio_file' in request.FILES:
        question.audio_file = request.FILES['audio_file']
        question.save()

    if 'video_file' in request.FILES:
        question.video_file = request.FILES['video_file']
        question.save()

def generate_wordcloud_image(text, font_path):
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

def validate_question_data(question_data, required_fields):
    for field in required_fields:
        if not question_data.get(field):
            raise ValidationError(f'{field.replace("_", " ").title()} is required.')

    return True