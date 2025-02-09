from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from django.contrib.auth.decorators import login_required
from user_management.helpers import role_required

import os
import matplotlib
matplotlib.use('Agg')

# PUT THIS IN A CLASS PLS BEFORE MERGING TO MAIN

from question_management.helpers import get_timer, save_files, generate_wordcloud_image, validate_question_data


@login_required
@role_required('Lecturer')
def add_question(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, user=request.user) # get object or 404
    if request.method == 'POST':
        question_type = request.POST.get('question_type')
        youtube_link = request.POST.get('youtube_link')
        timer = get_timer(request)

        question_data = {
            'poll': poll,
            'poll_id': poll_id,
            'question_text': request.POST.get('question_text'),
            'question_type': question_type,
            'youtube_link': youtube_link,
            'timer': timer
        }

        try:
            # Validate required fields for each question type
            if question_type == "multiple_choice":
                validate_question_data(request.POST, ['multiple_choice_options', 'multiple_choice_answers'])
            elif question_type == "single_choice":
                validate_question_data(request.POST, ['single_choice_options', 'single_choice_answers'])
            elif question_type == "text_fill":
                validate_question_data(request.POST, ['text_fill_answer'])
            elif question_type == "dropdown_fill":
                validate_question_data(request.POST, ['dropdown_correct_answer'])
            elif question_type == "match_question":
                validate_question_data(request.POST, ['match_question_options', 'match_question_answers'])

            question = Question.objects.create(**question_data)

            save_files(request, question)  # Save audio and video files if present

            # Handle wordcloud separately due to unique logic
            if question_type == 'wordcloud':

                text = ("Testing Testing the Word Cloud hello hello hello SEG SEG SEG wow amazing great yay woohoo "
                        "Hello Soumia Soumia Amina Amina Leyli Leyli Eeshal Marium Rashida Rashida Alishba Alishba Alishba")
                font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                         "static/fonts/RobotoMono-Regular.ttf")
                wordcloud_image = generate_wordcloud_image(text, font_path)

                return render(request, "add_question.html", {"poll": poll, "wordcloud_image": wordcloud_image})

            # Handle other types of questions after creation
            question.save()

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Save the question instance
        return redirect("question_management:add_question", poll_id=poll.id)

    return render(request, "add_question.html", {"poll": poll})



