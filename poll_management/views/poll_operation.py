from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from poll_management.models.poll_model import Poll

@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, user=request.user)
    return render(request, 'poll_results.html', {'poll': poll})

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
    poll = get_object_or_404(Poll, id=poll_id, user=request.user)
    if request.method == 'POST':
        poll.delete()
        return redirect('user_management:dashboard')
    return render(request, 'poll_delete.html', {'poll': poll})

@login_required
def poll_lock(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')  # Get the action from the button pressed
        lock_or_unlock(request, action, poll)
        return redirect(reverse('user_management:dashboard'))

    return render(request, 'lock_poll_confirmation.html', {'poll': poll})

def lock_or_unlock(request, action, poll):
    if action == 'lock':
        poll.locked = True
        poll.status = 'closed'
        messages.success(request, f"The poll '{poll.title}' has been locked successfully.")
    elif action == 'unlock':
        poll.locked = False
        poll.status = 'active'
        messages.success(request, f"The poll '{poll.title}' has been unlocked successfully.")

    poll.save()