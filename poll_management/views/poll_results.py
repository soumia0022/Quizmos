from django.shortcuts import render, get_object_or_404

from poll_management.models.poll_model import Poll


from user_management.helpers import role_required


@role_required('Student')
def poll_results(request, code):
    poll = get_object_or_404(Poll, number_code=code)

    return render(request, 'poll_results.html', {'poll': poll})
