from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from question_management.views import QuestionManager
from poll_management.models.poll_model import Poll
from question_management.helpers import get_timer
from user_management.helpers import role_required

@login_required
@role_required('Lecturer')
def add_question(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, user=request.user)

    if request.method == 'POST':
        # Update Poll Title
        new_title = request.POST.get('poll_title') or request.POST.get('poll_title_hidden')
        if new_title and new_title != poll.title:
            poll.title = new_title
            poll.save()

        manager = QuestionManager(request, poll_id, request.POST.get('youtube_link'), get_timer(request))

        response = None #if a manager is not created then there is no response. a manager isn't created if you're just changing the poll title

        if manager.question_type == 'text_fill':
            response = manager.handle_text_fill()
        elif manager.question_type == 'dropdown_fill':
            response = manager.handle_dropdown_fill()
        elif manager.question_type == 'multiple_choice':
            response = manager.handle_multiple_choice()
        elif manager.question_type == 'single_choice':
            response = manager.handle_single_choice()
        elif manager.question_type == 'wordcloud':
            wordcloud_image = manager.handle_wordcloud()
            return render(request, "add_question.html", {"poll": poll, "wordcloud_image": wordcloud_image})
        elif manager.question_type == 'match_question':
            response = manager.handle_match_question()
        elif manager.question_type == "code_question":
            response = manager.handle_code_question()

        if isinstance(response, JsonResponse):  # If the response is a JsonResponse (error validation - no redirect)
            return response

        return redirect("question_management:add_question", poll_id=poll.id)

    return render(request, "add_question.html", {"poll": poll})