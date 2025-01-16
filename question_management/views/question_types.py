from django.shortcuts import render, redirect
from question_management.models.question_models import Poll, Question

# put this in poll_management app
def create_poll(request):
    if request.method == "POST":
        title = request.POST.get("title")
        poll = Poll.objects.create(title=title)
        return redirect("add_question", poll_id=poll.id)
    return render(request, "create_poll.html")

def add_question(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if request.method == 'POST':
        question_type = request.POST.get('question_type')

        # Get the relevant question fields based on question type
        if question_type == 'text_fill':
            question_text = request.POST.get('text_fill_question')
            question = Question.objects.create(
                poll_id=poll_id,
                question_type=question_type,
                text_fill_question=question_text
            )
        elif question_type == 'dropdown_fill':
            question_text = request.POST.get('dropdown_fill_question') # generalised (may be needed later)
            dropdown_question = request.POST.get('dropdown_fill_question') # specific
            dropdown_options = request.POST.get('dropdown_options')
            question = Question.objects.create(
                poll_id=poll_id,
                question_text=question_text,
                question_type=question_type,
                dropdown_fill_question=dropdown_question,
                dropdown_options=dropdown_options
            )
        elif question_type == 'multiple_choice':
            question_text = request.POST.get('multiple_choice_question')
            multiple_choice_question = request.POST.get('multiple_choice_question')
            multiple_choice_options = request.POST.get('multiple_choice_options')
            question = Question.objects.create(
                poll_id=poll_id,
                question_text=question_text,
                question_type=question_type,
                multiple_choice_question=multiple_choice_question,
                multiple_choice_options=multiple_choice_options
            )
        elif question_type == 'single_choice':
            question_text = request.POST.get('single_choice_question')
            single_choice_question = request.POST.get('single_choice_question')
            single_choice_option = request.POST.get('single_choice_option')
            question = Question.objects.create(
                poll_id=poll_id,
                question_text=question_text,
                question_type=question_type,
                single_choice_question=single_choice_question,
                single_choice_option=single_choice_option
            )

        # Save the question instance
        question.save()
        return redirect("add_question", poll_id=poll.id)
    return render(request, "add_question.html", {"poll": poll})


def preview_question(request, question_id):
    question = Question.objects.get(id=question_id)
    correct = None  # Default value

    if request.method == "POST":
        student_answer = request.POST.get("student_answer")
        correct = student_answer.strip().lower() == question.correct_answer.strip().lower()

    return render(request, "preview_question.html", {"question": question, "correct": correct})

