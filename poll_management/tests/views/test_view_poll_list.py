from django.test import TestCase
from django.urls import reverse
from poll_management.models.poll_model import Poll
from user_management.models import User

class PollListViewTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='password', role='Lecturer')
        Poll.objects.create(title='Poll 1', user=self.user, status='active')
        Poll.objects.create(title='Poll 2', user=self.user, status='closed')

    def test_poll_list_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('user_management:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Poll 1')
        self.assertContains(response, 'Poll 2')