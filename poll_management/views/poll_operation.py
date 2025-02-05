from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from poll_management.models.poll_model import Poll


@login_required
def view_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'view_poll.html', {'poll': poll})

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
    if request.method == 'POST':
        poll = get_object_or_404(Poll, id=poll_id, user=request.user)
        poll.delete()
        return redirect('user_management:dashboard') 
    else:
        return redirect('user_management:dashboard')

