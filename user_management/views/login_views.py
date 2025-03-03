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
    """Display the current user's dashboard."""
    
    current_user = request.user

    if current_user.first_name == "Guest":
        user_id = current_user.id
        logout(request)

        # Import the User model and delete the guest user
        User = get_user_model()
        User.objects.filter(id=user_id).delete()

        return redirect('user_management:home')
    
    if current_user.role == 'Student':
        # Search and sort for students
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', 'created_at_desc')
        joined_polls = current_user.joined_polls.all()

        if search_query:
            joined_polls = joined_polls.filter(Q(title__icontains=search_query))
        if sort_by == 'title_asc':
            joined_polls = joined_polls.order_by(Lower('title'))
        elif sort_by == 'title_desc':
            joined_polls = joined_polls.order_by(Lower('title').desc())
        elif sort_by == 'created_at_asc':
            joined_polls = joined_polls.order_by('created_at')
        elif sort_by == 'created_at_desc':
            joined_polls = joined_polls.order_by('-created_at')

        # Paginate after sorting and searching
        paginator = Paginator(joined_polls, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'student_dashboard.html', {'user': current_user, 'polls': page_obj, 'search_query': search_query, 'sort_by': sort_by})
    else:
        create_poll(request)
        
        sort_by = request.GET.get('sort_by', 'created_at_desc')  # Default sorting
        search_query = request.GET.get('search', '')  # Get the search query

        poll = Poll.objects.filter(user=request.user).annotate(
            multiple_choice_responses_count=Count('multiplechoiceresponse'),
            single_choice_responses_count=Count('singlechoiceresponse'),
            dropdown_fill_responses_count=Count('dropdownfillresponse'),
            text_fill_responses_count=Count('textfillresponse'),
            match_question_responses_count=Count('matchquestionresponse')
        )

        # Filtering based on search query
        if search_query:
            poll = poll.filter(Q(title__icontains=search_query))

        # Sorting logic based on sort_by parameter
        if sort_by == 'title_asc':
            poll = poll.order_by(Lower('title'))
        elif sort_by == 'title_desc':
            poll = poll.order_by(Lower('title').desc()) #can't use default '-' for sorting because it's case sensitive
        elif sort_by == 'created_at_asc':
            poll = poll.order_by('created_at')
        elif sort_by == 'created_at_desc':
            poll = poll.order_by('-created_at')

        # Add up all response counts for each poll
        for p in poll:
            p.total_responses_count = (
                p.multiple_choice_responses_count +
                p.single_choice_responses_count +
                p.dropdown_fill_responses_count +
                p.text_fill_responses_count +
                p.match_question_responses_count
            )

         #This where I paginate the polls
        paginator = Paginator(poll, 10)
        page_number = request.GET.get('page')  # Getting the page number
        page_obj = paginator.get_page(page_number)  # Getting the page object

        # Essentially rendering the template
        return render(request, 'lecturer_dashboard.html', {
            'user': current_user,
            'polls': page_obj,
            'sort_by': sort_by,
            'search_query': search_query,
        })


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