from django.test import TestCase
from django.urls import reverse
from poll_management.models.poll_model import Poll
from django.contrib.auth import get_user_model

class PollListViewTest(TestCase):
    def setUp(self):
        # Use the custom user model
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password')
        Poll.objects.create(title='Poll 1', user=self.user, status='active')
        Poll.objects.create(title='Poll 2', user=self.user, status='closed')

    def test_poll_list_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('poll_management:poll_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Poll 1')
        self.assertContains(response, 'Poll 2')