from django.conf import settings
from django.shortcuts import redirect
from django.http import Http404
from functools import wraps
from django.contrib.auth import get_user_model
from django.contrib.auth import login
import uuid

def custom_guest_user(view_func):
    """Decorator for view functions that creates guest users"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            User = get_user_model()
            # Generate a unique username and email
            unique_id = str(uuid.uuid4())[:8]
            username = f'guest_{unique_id}'
            email = f'guest_{unique_id}@temporary.com'


            guest_user = User.objects.create_user(
                username=username,
                email=email,
                password=None,
                first_name='Guest',# to identify guests
                last_name=unique_id,
                role='Student'
            )

            guest_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, guest_user)

        return view_func(request, *args, **kwargs)

    return wrapper

def login_prohibited(view_function):
    """Decorator for view functions that redirect users away if they are logged in."""

    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)

    return modified_view_function

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view_func(request, *args, **kwargs):
            if request.user.role != required_role:
                 raise Http404
            return view_func(request, *args, **kwargs)
        return _wrapped_view_func
    return decorator
