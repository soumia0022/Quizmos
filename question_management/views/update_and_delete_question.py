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

        # send the updated timer field (called question_timer in html)
        question.timer = request.POST.get("question_timer")
        #print(question.timer)

        # Save options based on question type
        if question.question_type == "multiple_choice":
            #replace the mc question
            question.multiple_choice_question = request.POST.get("question_text")

            question.multiple_choice_options = request.POST.getlist("multiple_choice_options[]")

            #don't need to append as the html checks if the original options are now marked as checked
            newAnswers = request.POST.getlist("multiple_choice_answers[]")
            question.multiple_choice_answers = newAnswers
            #print("answers:", question.multiple_choice_answers)

            #TO DO: add contraints options or answers can't be empty

        elif question.question_type == "single_choice":
            # replace the sc question
            question.single_choice_question = request.POST.get("question_text")

            question.single_choice_option = request.POST.getlist("single_choice_options[]")

            # don't need to append as the html checks if the original options are now marked as checked
            question.single_choice_answers = request.POST.getlist("single_choice_answers[]")
            print("answers:", question.single_choice_answers)

            # TO DO: add contraints options or answers can't be empty
            # TO DO: there can onyl be 1 answer

        elif question.question_type == "text_fill":
            question.text_fill_question = request.POST.get("question_text")
            #print("text fill question:", question.text_fill_question)
            question.text_fill_answer = request.POST.get("text_fill_answer")
            #print("text fill answer:", question.text_fill_answer)


        elif question.question_type == "dropdown_fill":
            question.dropdown_options = ','.join(request.POST.getlist("dropdown_options[]"))
            question.dropdown_correct_answer = request.POST.get("dropdown_correct_answer", "")

        elif question.question_type == "wordcloud":
            question.wordcloud_question = request.POST.get("question_text")

        elif question.question_type == "match_question":
            question.match_question = request.POST.get("question_text")
            question.match_options = request.POST.getlist("match_question_options[]")
            question.match_answers = request.POST.getlist("match_question_answers[]")


        question.save()
        return redirect("question_management:add_question", poll_id=poll.id)

    dropdown_options = question.dropdown_options.split(',') if question.dropdown_options else []
    #print(dropdown_options)
    context = {
        'question': question,
        'dropdown_options': dropdown_options,
    }
    return render(request, 'edit_question.html', context)


def delete_question(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    question_id = request.GET.get("question_id")  # Get question_id from query params
    question = get_object_or_404(Question, id=question_id, poll=poll)

    question.delete()

    return redirect("question_management:add_question", poll_id=poll.id)