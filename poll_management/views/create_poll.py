from django.shortcuts import redirect, render

from poll_management.models.poll_model import Poll

def create_poll(request):
    if request.method == "POST":
        title = request.POST.get("title")
        poll = Poll.objects.create(title=title)
        # return redirect("add_question", poll_id=poll.id) # Needs to be put back in (question_management part)
    return render(request, "create_poll.html")
