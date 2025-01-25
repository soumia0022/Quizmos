from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from poll_management.models.poll_model import Poll

def join_poll(request, code):
    poll = get_object_or_404(Poll, number_code=code)
    if request.method == 'POST':
        # Handle student joining the poll
        # Send WebSocket message to update the board
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'poll_{poll.number_code}',
            {
                'type': 'poll_message',
                'message': f'A student joined the poll: {poll.title}!'
            }
        )
        return redirect('poll_management:poll_results', code=poll.number_code)
    return render(request, 'join_poll.html', {'poll': poll})
