from django.conf import settings
from django.shortcuts import redirect
from django.http import Http404
from functools import wraps


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
