from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from question_management.views.edit_question_manager import QuestionManager

class EditQuestionView(View):
    def get(self, request, poll_id):
        """Handles GET request to render the edit question page."""
        poll = get_object_or_404(Poll, id=poll_id)
        question_id = request.GET.get("question_id")
        question = get_object_or_404(Question, id=question_id, poll=poll)

        # Prepare context for rendering the edit page
        dropdown_options = question.dropdown_options.split(',') if question.dropdown_options else []
        match_pairs = zip(question.match_options, question.match_answers)
        context = {
            'question': question,
            'dropdown_options': dropdown_options,
            'match_pairs': match_pairs,
        }
        return render(request, 'edit_question.html', context)

    def post(self, request, poll_id):
        """Handles POST request to edit the question."""
        poll = get_object_or_404(Poll, id=poll_id)
        question_id = request.GET.get("question_id")
        question = get_object_or_404(Question, id=question_id, poll=poll)

        question.question_text = request.POST.get("question_text")
        question.question_timer = request.POST.get("question_timer")

        validation_response = None
        if question.question_type == "multiple_choice":
            question.multiple_choice_question = request.POST.get("question_text")
            question.multiple_choice_options = request.POST.getlist("multiple_choice_options[]")
            question.multiple_choice_answers = request.POST.getlist("multiple_choice_answers[]")
            validation_response = QuestionManager.validate_multiple_choice(question)

        elif question.question_type == "single_choice":
            question.single_choice_question = request.POST.get("question_text")
            question.single_choice_option = request.POST.getlist("single_choice_options[]")
            question.single_choice_answers = request.POST.getlist("single_choice_answers[]")
            validation_response = QuestionManager.validate_single_choice(question)

        elif question.question_type == "text_fill":
            question.text_fill_question = request.POST.get("question_text")
            question.text_fill_answer = request.POST.get("text_fill_answer")
            validation_response = QuestionManager.validate_text_fill(question)

        elif question.question_type == "dropdown_fill":
            question.dropdown_options = ','.join(request.POST.getlist("dropdown_options[]"))
            question.dropdown_correct_answer = request.POST.get("dropdown_correct_answer", "")
            validation_response = QuestionManager.validate_dropdown_fill(question)

        elif question.question_type == "wordcloud":
            question.wordcloud_question = request.POST.get("question_text")
            validation_response = QuestionManager.validate_wordcloud(question)

        elif question.question_type == "match_question":
            question.match_question = request.POST.get("question_text")
            question.match_options = request.POST.getlist("match_question_options[]")
            question.match_answers = request.POST.getlist("match_question_answers[]")
            validation_response = QuestionManager.validate_match_question(question)

        elif question.question_type == "code_question":
            question.code_question = request.POST.get("question_text")
            question.code_language = request.POST.get("code_language")
            question.correct_code = request.POST.get("correct_code")

        if validation_response:
            return validation_response

        question.save()
        return redirect("question_management:add_question", poll_id=poll.id)