import base64
import time
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from django.contrib.auth.decorators import login_required
from user_management.helpers import role_required 

import os, io

from collections import Counter
from django.http import HttpResponse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import ImageFont
import matplotlib
matplotlib.use('Agg')

# FOR REFACTORING, BELOW THE QUESTION_TEXT AND THE SPECIFIC QUESTIONS HAVE THE SAME LINE (SAME THING)
# PUT THIS IN A CLASS PLS BEFORE MERGING TO MAIN
# MAKE TEMPLATES FOLDER A DIRECTORY NOT A PACKAGE!!

def get_timer(request):
    timer = request.POST.get('question_timer')

    if not timer:
        timer = None
    else:
        try:
            timer = int(timer)
        except ValueError:
            timer = None

    return timer

@login_required
@role_required('Lecturer')
def add_question(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, user=request.user) # get object or 404
    if request.method == 'POST':
        question_type = request.POST.get('question_type')
        youtube_link = request.POST.get('youtube_link')

        # Get the relevant question fields based on question type:

        if question_type == 'text_fill': # E.g., 'What is an apple?', 'a fruit' (as text, not as an option)
            question_text = request.POST.get('text_fill_question')
            question_answer = request.POST.get('text_fill_answer')
            timer = get_timer(request)
            question = Question.objects.create(
                poll_id=poll_id,
                question_text=question_text,
                question_type=question_type,
                text_fill_question=question_text,
                text_fill_answer=question_answer,
                # audio_file=audio_file,
                # video_file=video_file,
                youtube_link=youtube_link,
                timer=timer
            )
            question.save()
            if 'audio_file' in request.FILES:
                question.audio_file = request.FILES['audio_file']
                question.save()

                # Handling the video file after the question is saved
            if 'video_file' in request.FILES:
                question.video_file = request.FILES['video_file']
                question.save()

        elif question_type == 'dropdown_fill':
            original_text = request.POST.get('dropdown_fill_question') # The original text that is inputted
            question_text = request.POST.get('dropdown_fill_question')
            correct_answer = request.POST.get('dropdown_correct_answer')
            additional_options = request.POST.getlist('additional_options')
            question_with_blank = original_text.replace(correct_answer, '_____') # The original text with blank to replace
            timer = get_timer(request)

            question = Question.objects.create(
                poll=poll,
                poll_id=poll_id,
                question_text=question_text,
                question_type=question_type,
                dropdown_fill_question=question_with_blank,
                dropdown_answer = correct_answer,
                dropdown_options=','.join([correct_answer] + additional_options),  # Store all options
                timer=timer,
                # audio_file=audio_file,
                # video_file=video_file,
                youtube_link=youtube_link
            )
            question.save()
            if 'audio_file' in request.FILES:
                question.audio_file = request.FILES['audio_file']
                question.save()

                # Handling the video file after the question is saved
            if 'video_file' in request.FILES:
                question.video_file = request.FILES['video_file']
                question.save()
        elif question_type == 'multiple_choice':
            question_text = request.POST.get('multiple_choice_question')
            multiple_choice_question = request.POST.get('multiple_choice_question')
            multiple_choice_options = request.POST.getlist('multiple_choice_options[]')
            multiple_choice_answers = request.POST.getlist('multiple_choice_answers[]')
            timer = get_timer(request)

            # Server-side validation
            if not multiple_choice_options:
                return JsonResponse({'error': 'At least one option is required for a multiple-choice question.'},
                                    status=400)
            if not multiple_choice_answers:
                return JsonResponse({'error': 'At least one answer is required for a multiple-choice question.'},
                                    status=400)

            question = Question.objects.create(
                poll_id=poll_id,
                question_text=question_text,
                question_type=question_type,
                multiple_choice_question=multiple_choice_question,
                multiple_choice_options=multiple_choice_options,
                multiple_choice_answers=multiple_choice_answers,
                timer=timer,
                # audio_file=audio_file,
                # video_file=video_file,
                youtube_link=youtube_link
            )
            question.save()
            if 'audio_file' in request.FILES:
                question.audio_file = request.FILES['audio_file']
                question.save()

                # Handling the video file after the question is saved
            if 'video_file' in request.FILES:
                question.video_file = request.FILES['video_file']
                question.save()
        elif question_type == 'single_choice':
            timer = get_timer(request)
            question_text = request.POST.get('single_choice_question')
            single_choice_question = request.POST.get('single_choice_question')
            single_choice_option = request.POST.getlist('single_choice_options[]')
            single_choice_answers = request.POST.get('single_choice_answers[]')

            # Server-side validation
            if not single_choice_option:
                return JsonResponse({'error': 'At least one option is required for a single-choice question.'},
                                    status=400)
            if not single_choice_answers:
                return JsonResponse({'error': 'At least one answer is required for a single-choice question.'},
                                    status=400)

            question = Question.objects.create(
                poll_id=poll_id,
                question_text=question_text,
                question_type=question_type,
                single_choice_question=single_choice_question,
                single_choice_option=single_choice_option,
                single_choice_answers=single_choice_answers,
                timer=timer,
                # audio_file=audio_file,
                # video_file=video_file,
                youtube_link=youtube_link
            )
            question.save()
            if 'audio_file' in request.FILES:
                question.audio_file = request.FILES['audio_file']
                question.save()

                # Handling the video file after the question is saved
            if 'video_file' in request.FILES:
                question.video_file = request.FILES['video_file']
                question.save()

        elif question_type == 'wordcloud':
            question_text = request.POST.get('wordcloud_question')
            timer = get_timer(request)

            question = Question.objects.create(
                poll_id=poll_id,
                question_text=question_text,
                question_type=question_type,
                wordcloud_question=question_text,
                timer=timer,
                # audio_file=audio_file,
                # video_file=video_file,
                youtube_link=youtube_link
            )
            question.save()

            if 'audio_file' in request.FILES:
                question.audio_file = request.FILES['audio_file']
                question.save()

                # Handling the video file after the question is saved
            if 'video_file' in request.FILES:
                question.video_file = request.FILES['video_file']
                question.save()

            text = ("Testing Testing the Word Cloud hello hello hello SEG SEG SEG wow amazing great yay woohoo "
                    "Hello Soumia Soumia Amina Amina Leyli Leyli Eeshal Marium Rashida Rashida Alishba Alishba Alishba")
            word_frequencies = Counter(text.split())

            font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                     "static/fonts/RobotoMono-Regular.ttf")

            # Later create html pages for the errors below (so it looks nice and fits UI, and user informed of error)
            if not os.path.exists(font_path):
                raise FileNotFoundError("Font file not found")
            else: # File has been found
                try:
                    font = ImageFont.truetype(font_path) # Font is TrueType
                except IOError:
                    raise ValueError("Only supported for TrueType fonts")
            matplotlib.use('Agg')
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                colormap='twilight',  # Colour scheme
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

            wordcloud_image = base64.b64encode(buffer.getvalue()).decode()
            return render(request, "add_question.html", {"poll": poll, "wordcloud_image": wordcloud_image})

        elif question_type == 'match_question':
            question_text = request.POST.get('match_question') #do we need this?
            match_question = request.POST.get('match_question')
            match_options = request.POST.getlist('match_question_options[]')
            match_answers = request.POST.getlist('match_question_answers[]')
            timer = get_timer(request)


            # Server-side validation
            if not match_options:
                return JsonResponse({'error': 'At least one option is required for a multiple-choice question.'},
                                    status=400)
            if not match_answers:
                return JsonResponse({'error': 'At least one answer is required for a multiple-choice question.'},
                                    status=400)

            question = Question.objects.create(
                poll_id=poll_id,
                question_text=question_text,
                question_type=question_type,
                match_question=match_question,
                match_options=match_options,
                match_answers=match_answers,
                timer=timer,
                # audio_file=audio_file,
                # video_file=video_file,
                youtube_link=youtube_link
            )


            #it saved (showed up in the admin view) even without this line?
            question.save()
            if 'audio_file' in request.FILES:
                question.audio_file = request.FILES['audio_file']
                question.save()

                # Handling the video file after the question is saved
            if 'video_file' in request.FILES:
                question.video_file = request.FILES['video_file']
                question.save()

        # Save the question instance
        return redirect("question_management:add_question", poll_id=poll.id)

    return render(request, "add_question.html", {"poll": poll})



