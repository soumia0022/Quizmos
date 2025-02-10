from django.shortcuts import get_object_or_404, redirect

from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question

def delete_question(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    question_id = request.GET.get("question_id")
    question = get_object_or_404(Question, id=question_id, poll=poll)
    question.delete()

    return redirect("question_management:add_question", poll_id=poll.id)