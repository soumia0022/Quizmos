from django.test import TestCase, Client
from django.urls import reverse
from poll_management.models.poll_model import Poll
from user_management.models import User

class CreatePollViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.create_url = reverse('poll_management:create_poll')

    def test_create_poll_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_poll.html')

    def test_create_poll_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'title': 'Sample Poll'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code,302)
        poll = Poll.objects.get(title='Sample Poll')
        self.assertIsNotNone(poll)
        self.assertEqual(poll.user, self.user)