from django.shortcuts import render
from django.http import JsonResponse
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
            question.multiple_choice_answers = request.POST.getlist("multiple_choice_answers[]")
            #print("answers:", question.multiple_choice_answers)

            # Server-side validation
            if not question.multiple_choice_options:
                return JsonResponse({'error': 'At least one option is required for a multiple-choice question.'},
                                    status=400)
            if not question.multiple_choice_answers:
                return JsonResponse({'error': 'At least one answer is required for a multiple-choice question.'},
                                    status=400)


        elif question.question_type == "single_choice":

            # replace the sc question

            question.single_choice_question = request.POST.get("question_text")

            question.single_choice_option = request.POST.getlist("single_choice_options[]")

            #print("options: ", question.single_choice_option)

            # don't need to append as the html checks if the original options are now marked as checked

            question.single_choice_answers = request.POST.getlist("single_choice_answers[]")

            #print("answers:", question.single_choice_answers)

            # Server-side validation

            if not question.single_choice_answers or question.single_choice_answers == ['']:
                return JsonResponse({'error': 'At least one answer is required for a single-choice question.'},

                                    status=400)

            if not question.single_choice_option or question.single_choice_option == ['']:
                return JsonResponse({'error': 'At least one option is required for a single-choice question.'},

                                    status=400)

            if len(question.single_choice_answers) > 1:
                return JsonResponse({'error': 'Only one answer is allowed for a single-choice question.'}, status=400)


        elif question.question_type == "text_fill":

            question.text_fill_question = request.POST.get("question_text")

            question.text_fill_answer = request.POST.get("text_fill_answer")

            # Server-side validation

            if not question.text_fill_question:
                return JsonResponse({'error': 'Question text is required'}, status=400)

            if not question.text_fill_answer:
                return JsonResponse({'error': 'Text fill answer is required'}, status=400)

            question.save()


        elif question.question_type == "dropdown_fill":

            question.dropdown_options = ','.join(request.POST.getlist("dropdown_options[]"))

            question.dropdown_correct_answer = request.POST.get("dropdown_correct_answer", "")

            # Server-side validation

            if not question.dropdown_options:
                return JsonResponse({'error': 'At least one option is required for a dropdown-fill question.'},
                                    status=400)

            if not question.dropdown_correct_answer:
                return JsonResponse({'error': 'A correct answer is required for a dropdown-fill question.'}, status=400)

            question.save()


        elif question.question_type == "wordcloud":

            question.wordcloud_question = request.POST.get("question_text")

            # Server-side validation

            if not question.wordcloud_question:
                return JsonResponse({'error': 'Question text is required for a wordcloud question.'}, status=400)

            question.save()


        elif question.question_type == "match_question":

            question.match_question = request.POST.get("question_text")

            question.match_options = request.POST.getlist("match_question_options[]")

            question.match_answers = request.POST.getlist("match_question_answers[]")

            # Server-side validation

            if not question.match_options:
                return JsonResponse({'error': 'At least one option is required for a match question.'}, status=400)

            if not question.match_answers:
                return JsonResponse({'error': 'At least one answer is required for a match question.'}, status=400)

            if len(question.match_options) != len(question.match_answers):
                return JsonResponse({'error': 'The number of options must match the number of answers.'}, status=400)

            question.save()

        question.save()
        return redirect("question_management:add_question", poll_id=poll.id)

    dropdown_options = question.dropdown_options.split(',') if question.dropdown_options else []
    match_pairs = zip(question.match_options, question.match_answers)
    #print(dropdown_options)
    context = {
        'question': question,
        'dropdown_options': dropdown_options,
        'match_pairs': match_pairs,
    }
    return render(request, 'edit_question.html', context)


def delete_question(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    question_id = request.GET.get("question_id")  # Get question_id from query params
    question = get_object_or_404(Question, id=question_id, poll=poll)

    question.delete()

    return redirect("question_management:add_question", poll_id=poll.id)