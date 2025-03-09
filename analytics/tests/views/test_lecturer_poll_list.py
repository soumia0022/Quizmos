# Will likely be deleted

from django.test import TestCase, Client
from django.urls import reverse
from user_management.models.user_model import User
from poll_management.models.poll_model import Poll


class LecturerPollListTestCase(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        """Set up test data for polls, questions, and responses."""
        self.client = Client()
        self.user = User.objects.get(username='johndoe')
        self.user.set_password('password')
        self.user.save()

        # Create polls for the lecturer user
        self.poll_1 = Poll.objects.create(title="Poll 1", user=self.user)
        self.poll_2 = Poll.objects.create(title="Poll 2", user=self.user)

        # Other user will have a poll that will not be listed for the lecturer
        self.other_user = User.objects.create_user(username='other_lecturer', password='password', email='other@example.com')
        self.poll_3 = Poll.objects.create(title="Poll 3", user=self.other_user)

    def test_lecturer_poll_list_view(self):
        """Test that the lecturer poll list view displays only the polls of the logged-in lecturer."""
        self.client.login(username='johndoe', password='password')
        url = reverse('lecturer_poll_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll_list.html')
        self.assertIn(self.poll_1, response.context['polls'])
        self.assertIn(self.poll_2, response.context['polls'])
        self.assertNotIn(self.poll_3, response.context['polls'])

    def test_no_polls_for_lecturer(self):
        """Test that the view returns an empty poll list if the lecturer has no polls."""
        user_with_no_polls = User.objects.create_user(username='no_polls_lecturer', password='password', email='nopolls@example.com')
        self.client.login(username='no_polls_lecturer', password='password')
        url = reverse('lecturer_poll_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll_list.html')
        self.assertEqual(len(response.context['polls']), 0)
