from django.shortcuts import render, get_object_or_404
from poll_management.models.poll_model import Poll

def poll_results(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    return render(request, 'poll_results.html', {'poll': poll})
