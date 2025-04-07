from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from poll_management.models.poll_model import Poll
class PollArchiveBaseView(LoginRequiredMixin, View):
    """Base class for poll archive operations"""

    def get_poll(self, request, poll_id):
        return get_object_or_404(Poll, id=poll_id, user=request.user)

    def handle_invalid_method(self):
        return JsonResponse({"status": "error", "message": "Invalid request method"})


class ArchivePollView(PollArchiveBaseView):
    """Class to archive a poll"""

    def post(self, request, poll_id):
        poll = self.get_poll(request, poll_id)
        poll.archived = True
        poll.archived_at = timezone.now()
        poll.save()
        messages.success(request, f'Poll "{poll.title}" has been archived.')
        return redirect('user_management:dashboard')

    def get(self, request, poll_id):
        return self.handle_invalid_method()


class UnarchivePollView(PollArchiveBaseView):
    """Class to unarchive a poll"""

    def post(self, request, poll_id):
        poll = self.get_poll(request, poll_id)
        poll.archived = False
        poll.archived_at = None
        poll.save()
        messages.success(request, f'Poll "{poll.title}" has been unarchived.')
        return redirect('user_management:dashboard')

    def get(self, request, poll_id):
        return self.handle_invalid_method()


class ToggleArchivePollView(PollArchiveBaseView):
    """Class to toggle a poll's archive status"""

    def post(self, request, poll_id):
        poll = self.get_poll(request, poll_id)
        poll.archived = not poll.archived
        poll.archived_at = timezone.now() if poll.archived else None
        poll.save()
        action = "archived" if poll.archived else "unarchived"
        messages.success(request, f'Poll "{poll.title}" has been {action}.')
        return redirect('user_management:dashboard')

    def get(self, request, poll_id):
        return self.handle_invalid_method()


class ArchivedPollsListView(LoginRequiredMixin, ListView):
    """Class to view archived polls with pagination and filtering"""
    model = Poll
    template_name = 'archived_polls.html'
    context_object_name = 'polls'
    paginate_by = 9

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        sort_by = self.request.GET.get('sort_by', '-archived_at')

        queryset = Poll.objects.filter(user=self.request.user, archived=True)

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        order_field = self._get_order_field(sort_by)
        return queryset.order_by(order_field)

    def _get_order_field(self, sort_by):
        sort_options = {
            'title_asc': 'title',
            'title_desc': '-title',
            'created_at_asc': 'created_at',
            'created_at_desc': '-created_at',
            '-archived_at': '-archived_at'
        }
        return sort_options.get(sort_by, '-archived_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort_by', '-archived_at')
        context['view_type'] = 'archived'
        return context