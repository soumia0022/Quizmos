from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.models.functions import Lower
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from user_management.forms import LogInForm, PollCodeForm
from user_management.helpers import login_prohibited
from poll_management.models.poll_model import Poll
from django.db.models import  Q, F
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render
from user_management.helpers import generate_suggested_title, delete_guest_user
from response_management.models.response_model import (
            MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse,
            DropdownFillResponse, MatchQuestionResponse, WordCloudResponse,
            CodeQuestionResponse
        )

@login_prohibited
def home(request):
    if request.method == 'POST':
        form = PollCodeForm(request.POST)
        if form.is_valid():
            valid, poll = form.validate_and_redirect()
            if valid:

                return redirect('poll_management:join_poll', code=poll.number_code)
    else:
        form = PollCodeForm()

    return render(request, 'home.html', {'form': form})

class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or request.session.get('poll_redirect_url') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or request.session.get('poll_redirect_url') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            if 'poll_redirect_url' in request.session:
                del request.session['poll_redirect_url']
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect(reverse('user_management:home'))

@login_required(login_url='user_management:log_in')
def student_polls_page(request):
    """View to display only the polls section for students."""
    current_user = request.user

    response_types = [
        MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse,
        DropdownFillResponse, MatchQuestionResponse, WordCloudResponse,
        CodeQuestionResponse
    ]

    poll_ids = set()
    for response_type in response_types:
        poll_ids.update(
            response_type.objects.filter(user=current_user)
            .values_list('poll_id', flat=True)
            .distinct()
        )

    polls = Poll.objects.filter(id__in=poll_ids)

    search_query = request.GET.get('search', '')
    if search_query:
        polls = polls.filter(title__icontains=search_query)

    sort_by = request.GET.get('sort_by', 'title_asc')
    sort_options = {
        'title_asc': F('title').asc(),
        'title_desc': F('title').desc()
    }
    polls = polls.order_by(sort_options.get(sort_by, F('title').asc()))

    paginator = Paginator(polls, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student_polls_page.html', {
        'polls': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
    })

@login_required(login_url='user_management:log_in')
def join_poll_page(request):
    """View for the standalone Join Poll page."""
    form = PollCodeForm()
    if request.method == 'POST':
        form = PollCodeForm(request.POST)  
        if form.is_valid():
            valid, poll = form.validate_and_redirect()
            if valid:
                return redirect('poll_management:join_poll', code=poll.number_code)
            
    return render(request, 'join_poll_page.html', {'form': form})
