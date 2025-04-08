from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
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


class DashboardView(LoginRequiredMixin, View):
    login_url = 'user_management:log_in'
    template_name_lecturer = 'lecturer_dashboard.html'
    template_name_student = 'student_dashboard.html'

    def get(self, request):
        current_user = request.user

        if current_user.first_name == "Guest":
            delete_guest_user(request, current_user.id)
            return redirect('user_management:home')

        if current_user.role == "Lecturer":
            return self.handle_lecturer_dashboard(request)
        elif current_user.role == "Student":
            return self.handle_student_dashboard(request)
        else:
            return redirect(reverse('user_management:dashboard'))

    def post(self, request):
        if "title" not in request.POST:
            return self.get(request)

        return self.handle_poll_creation(request)

    def handle_poll_creation(self, request):
        title = request.POST.get("title", "").strip()
        confirmed = request.POST.get("confirmed", "false") == "true"
        existing_polls = Poll.objects.filter(user=request.user)
        existing_titles = {poll.title for poll in existing_polls}

        if title in existing_titles and not confirmed:
            suggested_title = generate_suggested_title(title, existing_titles)
            context = {
                'user': request.user,
                'polls': existing_polls,
                'show_confirmation_popup': True,
                'original_title': title,
                'suggested_title': suggested_title,
            }
            return render(request, self.template_name_lecturer, context)

        final_title = title if title not in existing_titles else generate_suggested_title(title, existing_titles)
        new_poll = Poll.objects.create(user=request.user, title=final_title)
        new_poll.save()
        return redirect('question_management:add_question', poll_id=new_poll.id)

    def handle_lecturer_dashboard(self, request):
        sort_by = request.GET.get('sort_by', 'created_at_desc')
        search_query = request.GET.get('search', '')

        polls = self.get_lecturer_polls(request.user, search_query, sort_by)
        page_obj = self.paginate_polls(polls, request.GET.get('page'))

        context = {
            'user': request.user,
            'polls': page_obj,
            'sort_by': sort_by,
            'search_query': search_query,
            'show_confirmation_popup': False,
            'original_title': "",
            'suggested_title': "",
        }
        return render(request, self.template_name_lecturer, context)

    def get_lecturer_polls(self, user, search_query, sort_by):
        polls = Poll.objects.filter(user=user, archived=False).annotate(
            multiple_choice_responses_count=Count('multiplechoiceresponse'),
            single_choice_responses_count=Count('singlechoiceresponse'),
            dropdown_fill_responses_count=Count('dropdownfillresponse'),
            text_fill_responses_count=Count('textfillresponse'),
            match_question_responses_count=Count('matchquestionresponse')
        )

        if search_query:
            polls = polls.filter(Q(title__icontains=search_query))

        sort_options = {
            'title_asc': Lower('title'),
            'title_desc': Lower('title').desc(),
            'created_at_asc': 'created_at',
            'created_at_desc': '-created_at'
        }

        polls = polls.order_by(sort_options.get(sort_by, '-created_at'))

        # Calculate total responses for each poll
        for poll in polls:
            poll.total_responses_count = (
                    poll.multiple_choice_responses_count +
                    poll.single_choice_responses_count +
                    poll.dropdown_fill_responses_count +
                    poll.text_fill_responses_count +
                    poll.match_question_responses_count
            )

        return polls

    def handle_student_dashboard(self, request):
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', 'title_asc')

        polls = self.get_student_polls(request.user, search_query, sort_by)
        page_obj = self.paginate_polls(polls, request.GET.get('page'))

        context = {
            'user': request.user,
            'polls': page_obj,
            'search_query': search_query,
            'sort_by': sort_by,
        }
        return render(request, self.template_name_student, context)

    def get_student_polls(self, user, search_query, sort_by):
        # Get all poll IDs where the student has responses
        poll_ids = self.get_student_response_poll_ids(user)
        polls = Poll.objects.filter(id__in=poll_ids)

        if search_query:
            polls = polls.filter(title__icontains=search_query)

        sort_options = {
            'title_asc': Lower('title'),
            'title_desc': Lower('title').desc()
        }
        polls = polls.order_by(sort_options.get(sort_by, Lower('title')))

        return polls

    def get_student_response_poll_ids(self, user):
        response_types = [
            MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse,
            DropdownFillResponse, MatchQuestionResponse, WordCloudResponse,
            CodeQuestionResponse
        ]

        poll_ids = set()
        for response_type in response_types:
            poll_ids.update(
                response_type.objects.filter(user=user)
                .values_list('poll_id', flat=True)
                .distinct()
            )

        return poll_ids

    def paginate_polls(self, polls, page_number):
        paginator = Paginator(polls, 12)
        return paginator.get_page(page_number)

@login_required(login_url='user_management:log_in')
def dashboard(request):
    view = DashboardView.as_view()
    return view(request)