from django.test import TestCase, Client
from django.urls import reverse
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User
from question_management.models.question_models import Question
from response_management.models.response_model import (
    MatchQuestionResponse, MultipleChoiceResponse, SingleChoiceResponse, DropdownFillResponse, TextFillResponse, WordCloudResponse
)
import json

class PollResultsViewTest(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='janedoe')
        self.poll = Poll.objects.create(title='Poll 1', user=self.user, number_code=111111)
        self.question_wordcloud = Question.objects.create(question_text='Enter your word(s)', poll=self.poll, question_type='wordcloud')
        
        self.poll_results_url = reverse('poll_management:poll_results', kwargs={'code': self.poll.number_code})

    def test_poll_results_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.poll_results_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll_results.html')
        self.assertContains(response, self.poll.title)

    def test_poll_not_found(self):
        self.client.force_login(self.user)
        url = reverse('poll_management:poll_results', kwargs={'code': 999999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_request_poll_results(self):
        self.client.force_login(self.user)
        response = self.client.get(self.poll_results_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll_results.html')
        self.assertContains(response, self.poll.title)

    
