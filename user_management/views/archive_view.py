from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from poll_management.models.poll_model import Poll
from django.contrib import messages
from django.core.paginator import Paginator
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
    """View archived polls with pagination and filtering"""
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', '-archived_at')  # Default sort by archive date

    archived_polls = Poll.objects.filter(user=request.user, archived=True)

    if search_query:
        archived_polls = archived_polls.filter(title__icontains=search_query)
    order_field = 'created_at'
    if sort_by == 'title_asc':
        order_field = 'title'
    elif sort_by == 'title_desc':
        order_field = '-title'
    elif sort_by == 'created_at_asc':
        order_field = 'created_at'
    elif sort_by == 'created_at_desc':
        order_field = '-created_at'



    archived_polls = archived_polls.order_by(order_field)

    paginator = Paginator(archived_polls, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'polls': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
        'view_type': 'archived'
    }

    return render(request, 'archived_polls.html', context)
