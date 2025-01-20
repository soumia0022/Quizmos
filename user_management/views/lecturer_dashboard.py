from django.shortcuts import render
from poll_management.models.poll_model import Poll
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required
def lecturer_dashboard(request):
    polls = Poll.objects.filter(user=request.user).annotate(
        responses_count=Count('responses') 
    ).order_by('-created_at')
    return render(request, 'poll_dashboard.html', {'polls': polls})