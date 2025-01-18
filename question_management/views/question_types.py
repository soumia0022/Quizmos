from django.shortcuts import render, redirect
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll


def add_question(request, poll_id):
    poll = Poll.objects.get(id=poll_id) # get object or 404
    if request.method == 'POST':
        question_type = request.POST.get('question_type')

        # Get the relevant question fields based on question type
        if question_type == 'text_fill':
            question_text = request.POST.get('text_fill_question')
            question_answer = request.POST.get('text_fill_answer')
            question = Question.objects.create(
                poll_id=poll_id,
                question_text=question_text,
                question_type=question_type,
                text_fill_question=question_text,
                text_fill_answer=question_answer
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
            multiple_choice_options = request.POST.getlist('multiple_choice_options[]')
            multiple_choice_answers = request.POST.getlist('multiple_choice_answers[]')

            question = Question.objects.create(
                poll_id=poll_id,
                question_text=question_text,
                question_type=question_type,
                multiple_choice_question=multiple_choice_question,
                multiple_choice_options=multiple_choice_options,
                multiple_choice_answers=multiple_choice_answers
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
        return redirect("question_management:add_question", poll_id=poll.id)
    return render(request, "add_question.html", {"poll": poll})


