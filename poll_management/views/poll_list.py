from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from poll_management.models.poll_model import Poll

@login_required
def poll_list(request):
    """View to list polls with response count."""
    polls = Poll.objects.filter(user=request.user).annotate(
        responses_count=Count('response')  
    ).order_by('-created_at')

    return render(request, 'poll_list.html', {'polls': polls})