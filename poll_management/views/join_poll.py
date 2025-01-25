from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404, render,redirect
from poll_management.models.poll_model import Poll

async def join_poll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.method == 'POST':
        # Handle student joining the poll
        # Send WebSocket message to update the board
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            f'poll_{pk}',
            {
                'type': 'poll_message',
                'message': f'A student joined the poll: {poll.title}!'
            }
        )
        return redirect('poll_management:poll_results', pk=pk)
    return render(request, 'join_poll.html', {'poll': poll})
