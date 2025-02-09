import json

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

from question_management.helpers import get_timer, save_files, generate_wordcloud_image, validate_question_options_and_answers

def create_question(request, poll_id, question_text, question_type, youtube_link, timer):
    question = Question.objects.create(
        poll_id=poll_id,
        question_text=question_text,
        question_type=question_type,
        youtube_link=youtube_link,
        timer=timer
    )
    return question

@login_required
@role_required('Lecturer')
def add_question(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, user=request.user) # get object or 404
    if request.method == 'POST':
        question_type = request.POST.get('question_type')
        youtube_link = request.POST.get('youtube_link')
        timer = get_timer(request)


        if question_type == 'text_fill':
            question_text = request.POST.get('text_fill_question')
            question = create_question(request, poll_id, question_text, question_type, youtube_link, timer)
            question.text_fill_answer = request.POST.get('text_fill_answer')
            question.text_fill_question = question_text
            question.save()
            save_files(request, question)

        elif question_type == 'dropdown_fill':
            original_text = request.POST.get('dropdown_fill_question') # The original text that is inputted
            question_text = original_text
            correct_answer = request.POST.get('dropdown_correct_answer')
            additional_options = request.POST.getlist('additional_options')
            question_with_blank = original_text.replace(correct_answer, '_____') # The original text with blank to replace

            question = create_question(request, poll_id, question_text, question_type, youtube_link, timer)
            question.dropdown_fill_question=question_with_blank
            question.dropdown_answer = correct_answer
            question.dropdown_options=','.join([correct_answer] + additional_options) # Store all options
            question.dropdown_correct_answer=correct_answer

            question.save()
            save_files(request, question)

        elif question_type == 'multiple_choice':
            question_text = request.POST.get('multiple_choice_question')
            multiple_choice_question = question_text
            multiple_choice_options = request.POST.getlist('multiple_choice_options[]')
            multiple_choice_answers = request.POST.getlist('multiple_choice_answers[]')

            validation_response = validate_question_options_and_answers(multiple_choice_options,
                                                                        multiple_choice_answers, "multiple_choice")
            if validation_response:
                return validation_response

            question = create_question(request, poll_id, question_text, question_type, youtube_link, timer)
            question.multiple_choice_answers = multiple_choice_answers
            question.multiple_choice_question = multiple_choice_question
            question.multiple_choice_options = multiple_choice_options
            question.save()
            save_files(request, question)


        elif question_type == 'single_choice':
            question_text = request.POST.get('single_choice_question')
            single_choice_question = question_text
            single_choice_option = request.POST.getlist('single_choice_options[]')
            single_choice_answers = request.POST.get('single_choice_answers[]')

            validation_response = validate_question_options_and_answers(single_choice_option, single_choice_answers,
                                                                        "single_choice")
            if validation_response:
                return validation_response

            question = create_question(request, poll_id, question_text, question_type, youtube_link, timer)
            question.single_choice_question=single_choice_question
            question.single_choice_option=single_choice_option
            question.single_choice_answers=single_choice_answers
            question.save()
            save_files(request, question)

        elif question_type == 'wordcloud':
            question_text = request.POST.get('wordcloud_question')
            question = create_question(request, poll_id, question_text, question_type, youtube_link, timer)
            question.wordcloud_question = question_text
            question.save()
            save_files(request, question)

            text = ("Testing Testing the Word Cloud hello hello hello SEG SEG SEG wow amazing great yay woohoo "
                    "Hello Soumia Soumia Amina Amina Leyli Leyli Eeshal Marium Rashida Rashida Alishba Alishba Alishba")

            font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                     "static/fonts/RobotoMono-Regular.ttf")

            wordcloud_image = generate_wordcloud_image(text, font_path)
            return render(request, "add_question.html", {"poll": poll, "wordcloud_image": wordcloud_image})

        elif question_type == 'match_question':
            question_text = request.POST.get('match_question')
            match_question = question_text
            match_options = request.POST.getlist('match_question_options[]')
            match_answers = request.POST.getlist('match_question_answers[]')

            validation_response = validate_question_options_and_answers(match_options, match_answers, "match_question")
            if validation_response:
                return validation_response

            question = create_question(request, poll_id, question_text, question_type, youtube_link, timer)
            question.match_question=match_question
            question.match_options=match_options
            question.match_answers=match_answers
            question.save()
            save_files(request, question)

        elif question_type == "code_question":
            question_text = request.POST.get("code_question_text", "")
            code_language = request.POST.get("code_language", "python")
            code_test_cases_raw = request.POST.get("code_test_cases", "[]")

            try:
                code_test_cases = json.loads(code_test_cases_raw)  # Parse test cases as JSON
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format for test cases."}, status=400)

            question = create_question(request, poll_id, question_text, question_type, youtube_link, timer)
            question.code_question_text=question_text
            question.code_language=code_language
            question.code_test_cases=code_test_cases
            question.save()
            save_files(request, question)

        # Save the question instance
        return redirect("question_management:add_question", poll_id=poll.id)

    return render(request, "add_question.html", {"poll": poll})



