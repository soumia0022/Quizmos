from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from poll_management.models.poll_model import Poll

@login_required
def poll_edit(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, user=request.user)
    if request.method == 'POST':
        poll.title = request.POST.get('title', poll.title)
        poll.status = request.POST.get('status', poll.status)
        poll.save()
        return redirect('user_management:dashboard')
    return render(request, 'poll_edit.html', {'poll': poll})

@login_required
def poll_delete(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == 'POST':
        if request.user.role == 'Student':
            # to remove the poll from the user's joined polls
            request.user.joined_polls.remove(poll)
        elif request.user.role == 'Lecturer' and poll.user == request.user:
            # Only delete the poll if the user is the owner (Lecturer)
            poll.delete()
        
        messages.success(request, "Poll has been successfully deleted.")
        return redirect('user_management:dashboard')
    else:
        return redirect('user_management:dashboard')

