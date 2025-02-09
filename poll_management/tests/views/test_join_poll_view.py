from django.test import TestCase, Client
from django.urls import reverse
from poll_management.models.poll_model import Poll
from user_management.models import User

class JoinPollViewTest(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', role='Lecturer')
        self.student = User.objects.get(username= 'janedoe')
        self.poll = Poll.objects.create(title='Poll 1', user=self.user, status='active', number_code = 111111)
        self.join_poll_url = reverse('poll_management:join_poll', kwargs={'code': self.poll.number_code})


    def test_join_poll_get_request(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.get(self.join_poll_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'join_poll.html')
        self.assertContains(response, self.poll.title)

    def test_join_poll_guest_get_request(self):
        response = self.client.get(self.join_poll_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'join_poll_guest.html')



    def test_join_poll_post_request(self):
        response = self.client.post(self.join_poll_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('poll_management:poll_results', kwargs={'code': self.poll.number_code}))