from django.test import TestCase, Client
from django.urls import reverse
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class PollResultsViewTest(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username = 'johndoe')
        self.poll = Poll.objects.create(title='Poll 1', user=self.user, status='active', number_code=111111)
        self.poll_results_url = reverse('poll_management:poll_results', kwargs={'code': self.poll.number_code})

    def test_poll_results_view(self):
        response = self.client.get(self.poll_results_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll_results.html')
        self.assertContains(response, self.poll.title)
