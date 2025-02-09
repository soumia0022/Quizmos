from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404, render,redirect, reverse
from user_management.helpers import custom_guest_user
from poll_management.models.poll_model import Poll


@custom_guest_user
def join_poll(request, code):
    #ask to login or continue as guest
    # if login redirect to result page after login in
    #if guest redirect to result page
    poll = get_object_or_404(Poll, number_code=code)


    if request.method == 'POST':
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'poll_{poll.number_code}',
            {
                'type': 'poll_message',
                'message': f'A student joined the poll: {request.user.username}!'
            }
        )
        return redirect('poll_management:poll_results', code=poll.number_code)

    #check guest user
    results_url = reverse('poll_management:poll_results', kwargs={'code': code})
    request.session['poll_redirect_url'] = results_url
    if request.user.first_name == 'Guest':
        return render(request, 'join_poll_guest.html',{'poll': poll, 'code': code})

    return render(request, 'join_poll.html', {'poll': poll})

