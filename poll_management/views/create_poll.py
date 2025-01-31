from django.shortcuts import redirect, render
from django.urls import reverse
from user_management.helpers import role_required 
from poll_management.models.poll_model import Poll

@role_required('Lecturer')
def create_poll(request):
    if request.method == "POST":
        title = request.POST.get("title")
        poll = Poll.objects.create(title=title, user=request.user)
        return redirect(reverse("question_management:add_question", kwargs={"poll_id": poll.id})) # Needs to be put back in (question_management part)
    return render(request, "create_poll.html")
