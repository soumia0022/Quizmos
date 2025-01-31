from django.shortcuts import render
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from django.shortcuts import render, get_object_or_404, redirect

def edit_question(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    question_id = request.GET.get("question_id")  # Get question_id from query params
    question = get_object_or_404(Question, id=question_id, poll=poll)

    if request.method == "POST":
        question.question_text = request.POST.get("question_text")

        # Save options based on question type
        if question.question_type == "multiple_choice":
            question.multiple_choice_question = request.POST.get("question_text")
            question.multiple_choice_options = request.POST.get("multiple_choice_options", "").split(',')
            question.multiple_choice_answers = request.POST.get("multiple_choice_answers", "").split(',')

        elif question.question_type == "single_choice":
            question.single_choice_question = request.POST.get("question_text")
            question.single_choice_option = request.POST.get("single_choice_option", "").split(',')
            question.single_choice_answers = request.POST.get("single_choice_answers", "")

        elif question.question_type == "dropdown_fill":
            question.dropdown_options = request.POST.get("dropdown_options", "")
            question.dropdown_correct_answer = request.POST.get("dropdown_correct_answer", "")

        question.save()
        return redirect("question_management:add_question", poll_id=poll.id)

    return render(request, 'edit_question.html', {'question': question})


def delete_question(request, poll_id):
    question_id = request.GET.get('question_id')