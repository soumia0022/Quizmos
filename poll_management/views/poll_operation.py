from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from poll_management.models.poll_model import Poll
from response_management.models.response_model import MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse, DropdownFillResponse, MatchQuestionResponse


@login_required
def view_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'view_poll.html', {'poll': poll})


@login_required
def student_view_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    student = request.user

    # responses:
    multiple_choice_responses = MultipleChoiceResponse.objects.filter(user=student, poll=poll)
    single_choice_responses = SingleChoiceResponse.objects.filter(user=student, poll=poll)
    text_fill_responses = TextFillResponse.objects.filter(user=student, poll=poll)
    dropdown_responses = DropdownFillResponse.objects.filter(user=student, poll=poll)
    match_responses = MatchQuestionResponse.objects.filter(user=student, poll=poll)

    responses_by_question = {}

    for question_id, response in responses_by_question.items():
        if response.question.youtube_link:
            response.question.youtube_link = response.question.youtube_link.replace("youtu.be/",
                                                                                    "www.youtube.com/embed/")

    for response in multiple_choice_responses:
        question = response.question
        responses_by_question[question.id] = {
            'type': 'multiple_choice',
            'selected_options': response.selected_options,
            'question': question,
            'submitted_on': response.submitted_on
        }

    for response in single_choice_responses:
        question = response.question
        responses_by_question[question.id] = {
            'type': 'single_choice',
            'selected_option': response.selected_option,
            'question': question,
            'submitted_on': response.submitted_on
        }

    for response in text_fill_responses:
        question = response.question
        responses_by_question[question.id] = {
            'type': 'text_fill',
            'answer_text': response.answer_text,
            'question': question,
            'submitted_on': response.submitted_on
        }

    for response in dropdown_responses:
        question = response.question
        responses_by_question[question.id] = {
            'type': 'dropdown',
            'selected_option': response.selected_option,
            'question': question,
            'submitted_on': response.submitted_on
        }

    for response in match_responses:
        question = response.question
        responses_by_question[question.id] = {
            'type': 'match',
            'match_responses': response.match_responses,
            'question': question,
            'submitted_on': response.submitted_on
        }

    return render(request, 'student_view_response/poll_response.html', {
        'poll': poll,
        'responses_by_question': responses_by_question
    })

@login_required
def poll_edit(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, user=request.user)
    if request.method == 'POST':
        poll.title = request.POST.get('title', poll.title)
        poll.status = request.POST.get('status', poll.status)
        poll.save()
        return redirect('poll_management:view_poll', poll_id=poll.id)
    return render(request, 'poll_edit.html', {'poll': poll})

@login_required
def poll_delete(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == 'POST':
        if request.user.role == 'Student':
            # to remove the the poll from the user's joined polls
            request.user.joined_polls.remove(poll)
        elif request.user.role == 'Lecturer' and poll.user == request.user:
            # Only delete the poll if the user is the owner (Lecturer)
            poll.delete()
        
        messages.success(request, "Poll has been successfully deleted.")
        return redirect('user_management:dashboard')
    else:
        return redirect('user_management:dashboard')

