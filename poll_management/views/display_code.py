from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from poll_management.models.poll_model import Poll

def display_code(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    return render(request, 'display_code.html', {'poll': poll, 'code':poll.number_code})