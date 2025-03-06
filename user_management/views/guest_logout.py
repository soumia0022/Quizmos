from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def logout_and_login(request):
    """Prevent guest users from logging out, but allow normal users"""
    next_url = request.GET.get('next', '')
    if request.user.is_authenticated and request.user.first_name == 'Guest':
        user = request.user
        user.delete()  # remove the guest user from database
        return redirect(reverse("user_management:home"))

    return redirect(f'{reverse("user_management:log_in")}?next={next_url}')