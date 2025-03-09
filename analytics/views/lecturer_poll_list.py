# Will likely be deleted due to change in functionality

from django.shortcuts import render
from poll_management.models.poll_model import Poll

def lecturer_poll_list(request):
    lecturer_polls = Poll.objects.filter(user=request.user)
    return render(request, 'poll_list.html', {'polls': lecturer_polls})
