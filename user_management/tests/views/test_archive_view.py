from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import User
from django.utils import timezone
from poll_management.models.poll_model import Poll
import json
from datetime import timedelta


class PollArchiveTests(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(
            username='johndoe',
        )

        self.poll1 = Poll.objects.create(
            title='Test Poll 1',
            user=self.user,
            created_at=timezone.now() - timedelta(days=5)
        )

        self.poll2 = Poll.objects.create(
            title='Test Poll 2',
            user=self.user,
            created_at=timezone.now() - timedelta(days=3)
        )

        self.archived_poll = Poll.objects.create(
            title='Already Archived Poll',
            user=self.user,
            archived=True,
            archived_at=timezone.now() - timedelta(days=1),
            created_at=timezone.now() - timedelta(days=7)
        )


        self.client = Client()
        self.client.force_login(self.user)

    def test_archive_poll(self):
        """Test archiving a poll"""
        url = reverse('user_management:archive_poll', args=[self.poll1.id])
        response = self.client.post(url)

        self.assertRedirects(response, reverse('user_management:dashboard'))
        self.poll1.refresh_from_db()

        self.assertTrue(self.poll1.archived)
        self.assertIsNotNone(self.poll1.archived_at)

    def test_unarchive_poll(self):
        """Test unarchiving a poll"""
        url = reverse('user_management:unarchive_poll', args=[self.archived_poll.id])
        response = self.client.post(url)


        self.assertRedirects(response, reverse('user_management:dashboard'))

        self.archived_poll.refresh_from_db()

        self.assertFalse(self.archived_poll.archived)
        self.assertIsNone(self.archived_poll.archived_at)

    def test_toggle_archive_poll(self):
        """Test toggling a poll's archive status"""
        url = reverse('user_management:toggle_archive_poll', args=[self.poll2.id])
        response = self.client.post(url)

        self.assertRedirects(response, reverse('user_management:dashboard'))

        self.poll2.refresh_from_db()

        self.assertTrue(self.poll2.archived)
        self.assertIsNotNone(self.poll2.archived_at)

        response = self.client.post(url)

        self.poll2.refresh_from_db()

        self.assertFalse(self.poll2.archived)
        self.assertIsNone(self.poll2.archived_at)

    def test_view_archived_polls(self):
        """Test viewing archived polls"""
        url = reverse('user_management:view_archived_polls')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['polls']), 1)
        self.assertEqual(response.context['polls'][0].title, 'Already Archived Poll')

    def test_invalid_request_method(self):
        """Test invalid request method returns error JSON"""
        url = reverse('user_management:archive_poll', args=[self.poll1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Invalid request method')

    def test_archived_polls_filtering_and_sorting(self):
        """Test filtering and sorting functionality for archived polls"""
        Poll.objects.create(
            title='Archive Search Test',
            user=self.user,
            archived=True,
            archived_at=timezone.now(),
            created_at=timezone.now() - timedelta(days=2)
        )

        url = reverse('user_management:view_archived_polls') + '?search=search'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['polls']), 1)
        self.assertTrue('Search' in response.context['polls'][0].title)

        url = reverse('user_management:view_archived_polls') + '?sort_by=title_asc'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        polls = list(response.context['polls'])
        if len(polls) > 1:
            self.assertTrue(polls[0].title < polls[1].title)