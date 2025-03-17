from django.shortcuts import render
from poll_management.models.poll_model import Poll

# DELETE THIS
def lecturer_poll_list(request):
    lecturer_polls = Poll.objects.filter(user=request.user)
    return render(request, 'poll_list.html', {'polls': lecturer_polls})
