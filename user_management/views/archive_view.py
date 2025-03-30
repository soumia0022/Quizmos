from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from poll_management.models.poll_model import Poll
from django.contrib import messages

@login_required
def archive_poll(request, poll_id):
    """Archive a poll"""
    poll = get_object_or_404(Poll, id=poll_id, user=request.user)
    if request.method == 'POST':
        poll.archived = True
        poll.archived_at = timezone.now()
        poll.save()
        messages.success(request, f'Poll "{poll.title}" has been archived.')
        return redirect('user_management:dashboard')
    return JsonResponse({"status": "error", "message": "Invalid request method"})


@login_required
def unarchive_poll(request, poll_id):
    """Unarchive a poll"""
    poll = get_object_or_404(Poll, id=poll_id, user=request.user)
    if request.method == 'POST':
        poll.archived = False
        poll.archived_at = None
        poll.save()
        messages.success(request, f'Poll "{poll.title}" has been unarchived.')
        return redirect('user_management:dashboard')
    return JsonResponse({"status": "error", "message": "Invalid request method"})


@login_required
def toggle_archive_poll(request, poll_id):
    """Toggle a poll's archive status"""
    poll = get_object_or_404(Poll, id=poll_id, user=request.user)
    if request.method == 'POST':
        poll.archived = not poll.archived
        poll.archived_at = timezone.now() if poll.archived else None
        poll.save()
        action = "archived" if poll.archived else "unarchived"
        messages.success(request, f'Poll "{poll.title}" has been {action}.')
        return redirect('user_management:dashboard')
    return JsonResponse({"status": "error", "message": "Invalid request method"})


@login_required
def view_archived_polls(request):
    """View archived polls"""
    archived_polls = Poll.objects.filter(user=request.user, archived=True).order_by('-archived_at')
    return render(request, 'archived_polls.html', {'polls': archived_polls, 'view_type': 'archived'})

