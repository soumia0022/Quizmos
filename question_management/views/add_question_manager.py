import json
from django.http import JsonResponse
import os
import matplotlib
matplotlib.use('Agg')

from question_management.models.question_models import Question
from question_management.helpers import generate_wordcloud_image, validate_question_options_and_answers

class QuestionManager:
    """Class-based view to handle the creation of different types of questions.

     The QuestionManager class is responsible for handling the creation of questions when a user wants to add a
     question to a poll. It creates a base question that contains the fields that every question consists of, and then
     sets the relevant fields to their values for the specific question type chosen.
     """

    def __init__(self, request, poll_id, youtube_link, question_timer):
        self.request = request
        self.poll_id = poll_id
        self.youtube_link = youtube_link
        self.question_timer = question_timer
        self.question = None
        self.question_type = request.POST.get('question_type')
        self.question_text = None

    def create_base_question(self, question_text):
        """Create a new question instance."""
        self.question = Question.objects.create(
            poll_id=self.poll_id,
            question_text=question_text,
            question_type=self.question_type,
            youtube_link=self.youtube_link,
            question_timer=self.question_timer
        )
        return self.question

    def save_files(self):
        """Save uploaded audio and video files."""
        for file_type in ['audio_file', 'video_file', 'image_file']:
            if file_type in self.request.FILES:
                setattr(self.question, file_type, self.request.FILES[file_type])
                self.question.save()

    def handle_text_fill(self):
        """Handle the creation of a text fill question."""
        question_text = self.request.POST.get('text_fill_question')
        self.create_base_question(question_text)
        self.question.text_fill_answer = self.request.POST.get('text_fill_answer')
        self.question.text_fill_question = question_text
        self.question.save()
        self.save_files()

    def handle_dropdown_fill(self):
        """Handle the creation of a dropdown_fill question."""
        original_text = self.request.POST.get('dropdown_fill_question')
        correct_answer = self.request.POST.get('dropdown_correct_answer')
        additional_options = self.request.POST.getlist('additional_options')
        question_with_blank = original_text.replace(correct_answer, '_____')

        self.create_base_question(original_text)
        self.question.dropdown_fill_question = question_with_blank
        self.question.dropdown_answer = correct_answer
        self.question.dropdown_options = ','.join([correct_answer] + additional_options)
        self.question.dropdown_correct_answer = correct_answer
        self.question.save()
        self.save_files()

    def handle_multiple_choice(self):
        """Handle the creation of a multiple choice question."""
        question_text = self.request.POST.get('multiple_choice_question')
        multiple_choice_options = self.request.POST.getlist('multiple_choice_options[]')
        multiple_choice_answers = self.request.POST.getlist('multiple_choice_answers[]')

        validation_response = validate_question_options_and_answers(multiple_choice_options, multiple_choice_answers, "multiple_choice")
        if validation_response:
            return validation_response

        self.create_base_question(question_text)
        self.question.multiple_choice_answers = multiple_choice_answers
        self.question.multiple_choice_question = question_text
        self.question.multiple_choice_options = multiple_choice_options
        self.question.save()
        self.save_files()

    def handle_single_choice(self):
        """Handle the creation of a single choice question."""
        question_text = self.request.POST.get('single_choice_question')
        single_choice_option = self.request.POST.getlist('single_choice_options[]')
        single_choice_answers = self.request.POST.get('single_choice_answers[]')

        validation_response = validate_question_options_and_answers(single_choice_option, single_choice_answers, "single_choice")
        if validation_response:
            return validation_response

        self.create_base_question(question_text)
        self.question.single_choice_question = question_text
        self.question.single_choice_option = single_choice_option
        self.question.single_choice_answers = single_choice_answers
        self.question.save()
        self.save_files()

    def handle_wordcloud(self):
        """Handle the creation of a word cloud question."""
        question_text = self.request.POST.get('wordcloud_question')
        self.create_base_question(question_text)
        self.question.wordcloud_question = question_text
        self.question.save()
        self.save_files()

        # Generate wordcloud image
        text = ("Testing Testing the Word Cloud hello hello hello SEG SEG SEG wow amazing great yay woohoo "
                "Hello Soumia Soumia Amina Amina Leyli Leyli Eeshal Marium Rashida Rashida Alishba Alishba Alishba")
        font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/fonts/RobotoMono-Regular.ttf")
        wordcloud_image = generate_wordcloud_image(text, font_path)

        return wordcloud_image

    def handle_match_question(self):
        """Handle the creation of a match question."""
        question_text = self.request.POST.get('match_question')
        match_options = self.request.POST.getlist('match_question_options[]')
        match_answers = self.request.POST.getlist('match_question_answers[]')

        validation_response = validate_question_options_and_answers(match_options, match_answers, "match_question")
        if validation_response:
            return validation_response

        self.create_base_question(question_text)
        self.question.match_question = question_text
        self.question.match_options = match_options
        self.question.match_answers = match_answers
        self.question.save()
        self.save_files()

    def handle_code_question(self):
        """Handle the creation of a coding question."""
        question_text = self.request.POST.get("code_question_text", "")
        code_language = self.request.POST.get("code_language", "python")
        correct_code = self.request.POST.get("correct_code", "")

        self.create_base_question(question_text)
        self.question.code_question_text = question_text
        self.question.code_language = code_language
        self.question.correct_code = correct_code
        self.question.save()
        self.save_files()