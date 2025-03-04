from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.db.models.functions import Lower
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from user_management.forms import LogInForm, PollCodeForm
from user_management.helpers import login_prohibited
from poll_management.models.poll_model import Poll
from django.db.models import Count, Q
from poll_management.views.create_poll import create_poll
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
import re
from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth import get_user_model

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

@login_required(login_url='user_management:log_in')

def dashboard(request):
    current_user = request.user
    show_confirmation_popup = False
    original_title = ""
    suggested_title = ""

    if current_user.first_name == "Guest":
        user_id = current_user.id
        logout(request)
        User = get_user_model()
        User.objects.filter(id=user_id).delete()
        return redirect('user_management:home')

    def generate_suggested_title(base_title, existing_titles):
        matching_polls = [p for p in existing_titles if p.startswith(base_title)]
        number_pattern = re.compile(r'\((\d+)\)')
        existing_numbers = []

        for poll_title in matching_polls:
            number_matches = number_pattern.findall(poll_title)
            if number_matches:
                existing_numbers.append(tuple(map(int, number_matches)))

        if not existing_numbers:
            return f"{base_title} (1)"

        if f"{base_title} (1)" not in existing_titles:
            return f"{base_title} (1)"

        existing_numbers.sort()
        next_number = 1
        while (next_number,) in existing_numbers:
            next_number += 1

        return f"{base_title} ({next_number})"

    if request.method == "POST" and "title" in request.POST:
        title = request.POST.get("title", "").strip()
        confirmed = request.POST.get("confirmed", "false") == "true"
        existing_polls = Poll.objects.filter(user=request.user)
        existing_titles = {poll.title for poll in existing_polls}

        if title in existing_titles and not confirmed:
            suggested_title = generate_suggested_title(title, existing_titles)
            show_confirmation_popup = True
            original_title = title
            return render(request, 'lecturer_dashboard.html', {
                'user': current_user,
                'polls': existing_polls,
                'show_confirmation_popup': show_confirmation_popup,
                'original_title': original_title,
                'suggested_title': suggested_title,
            })

        new_poll_title = title if title not in existing_titles else generate_suggested_title(title, existing_titles)
        new_poll = Poll.objects.create(user=request.user, title=new_poll_title)
        new_poll.save()
        return redirect(reverse('user_management:dashboard'))

    sort_by = request.GET.get('sort_by', 'created_at_desc')
    search_query = request.GET.get('search', '')

    if current_user.role == "Lecturer":
        polls = Poll.objects.filter(user=request.user).annotate(
            multiple_choice_responses_count=Count('multiplechoiceresponse'),
            single_choice_responses_count=Count('singlechoiceresponse'),
            dropdown_fill_responses_count=Count('dropdownfillresponse'),
            text_fill_responses_count=Count('textfillresponse'),
            match_question_responses_count=Count('matchquestionresponse')
        )

        if search_query:
            polls = polls.filter(Q(title__icontains=search_query))

        sort_options = {
            'title_asc': 'title',
            'title_desc': '-title',
            'created_at_asc': 'created_at',
            'created_at_desc': '-created_at'
        }
        polls = polls.order_by(sort_options.get(sort_by, '-created_at'))

        for p in polls:
            p.total_responses_count = (
                p.multiple_choice_responses_count +
                p.single_choice_responses_count +
                p.dropdown_fill_responses_count +
                p.text_fill_responses_count +
                p.match_question_responses_count
            )

        paginator = Paginator(polls, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'lecturer_dashboard.html', {
            'user': current_user,
            'polls': page_obj,
            'sort_by': sort_by,
            'search_query': search_query,
            'show_confirmation_popup': show_confirmation_popup,
            'original_title': original_title,
            'suggested_title': suggested_title,
        })

    elif current_user.role == "Student":
        joined_polls = current_user.joined_polls.all()

        if search_query:
            joined_polls = joined_polls.filter(Q(title__icontains=search_query))

        sort_options = {
            'title_asc': Lower('title'),
            'title_desc': Lower('title').desc(),
            'created_at_asc': 'created_at',
            'created_at_desc': '-created_at'
        }

        joined_polls = joined_polls.order_by(sort_options.get(sort_by, '-created_at'))

        paginator = Paginator(joined_polls, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'student_dashboard.html', {
            'user': current_user,
            'polls': page_obj,
            'search_query': search_query,
            'sort_by': sort_by,
        })

    else:
        return redirect(reverse('user_management:dashboard'))


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