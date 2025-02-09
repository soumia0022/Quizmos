from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

def logout_and_login(request):
    """Handle logout of guest and redirect to login"""
    next_url = request.GET.get('next', '')
    if request.user.is_authenticated and request.user.first_name == 'Guest':
        # delete the guest user
        user = request.user
        logout(request)
        user.delete()  # remove the guest user from database
    return redirect(f'{reverse("user_management:log_in")}?next={next_url}')