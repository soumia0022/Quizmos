from django.conf import settings
from django.shortcuts import redirect
from django.http import Http404
from functools import wraps
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from user_management.models import User
import uuid
import random
import re
from django.contrib.auth import logout

def generate_suggested_title(base_title, existing_titles):
    pattern = re.compile(f"^{re.escape(base_title)}(?: \\((\\d+)\\))?$")

    existing_numbers = []
    for title in existing_titles:
        match = pattern.match(title)
        if match and match.group(1):
            existing_numbers.append(int(match.group(1)))

    if base_title not in existing_titles and not existing_numbers:
        return base_title

    if f"{base_title} (1)" not in existing_titles:
        return f"{base_title} (1)"

    existing_numbers.sort()
    next_number = 1
    while next_number in existing_numbers:
        next_number += 1

    return f"{base_title} ({next_number})"
def generate_guest_user_name():
    first_words = ["Nebula", "Star", "Galactic", "Cosmic", "Astral", "Lunar", "Solar", "Celestial"]
    second_words = ["Nomad", "Seeker", "Traveler", "Voyager", "Adventurer", "Explorer", "Surfer", "Chaser"]
    first = random.choice(first_words)
    second = random.choice(second_words)
    unique_id = str(uuid.uuid4())[:8]
    return f"{first}{second}{unique_id}"

def custom_guest_user(view_func):
    """Decorator for view functions that creates guest users"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            User = get_user_model()

            username = generate_guest_user_name()
            email = f'guest_{username}@temporary.com'


            guest_user = User.objects.create_user(
                username=username,
                email=email,
                password=None,
                first_name='Guest',# to identify guests
                last_name='Guest',
                role='Student'
            )

            guest_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, guest_user)

        return view_func(request, *args, **kwargs)

    return wrapper

def delete_guest_user(request, user_id):
    logout(request)
    User.objects.filter(id=user_id).delete()

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
