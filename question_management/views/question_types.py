from django.shortcuts import render, redirect
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll

# FOR REFACTORING, BELOW THE QUESTION_TEXT AND THE SPECIFIC QUESTIONS HAVE THE SAME LINE (SAME THING)
# PUT THIS IN A CLASS PLS BEFORE MERGING TO MAIN
# MAKE TEMPLATES FOLDER A DIRECTORY NOT A PACKAGE!!

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
            original_text = request.POST.get('dropdown_fill_question') # THE ORIGINAL TEXT THE LECTURER INPUTS
            question_text = request.POST.get('dropdown_fill_question') # generalised (maybe needed later)
            dropdown_question = request.POST.get('dropdown_fill_question') # specific
            dropdown_options = request.POST.get('dropdown_options')
            correct_answer = request.POST.get('dropdown_correct_answer')
            additional_options = request.POST.getlist('additional_options')

            question_with_blank = original_text.replace(correct_answer, '_____')

            question = Question.objects.create(
                poll=poll,
                poll_id=poll_id,
                question_text=question_text,
                question_type=question_type,
                dropdown_fill_question=question_with_blank,
                dropdown_options=','.join([correct_answer] + additional_options)  # Store all options
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
        return redirect("question_management:add_question", poll_id=poll.id)
    return render(request, "add_question.html", {"poll": poll})


