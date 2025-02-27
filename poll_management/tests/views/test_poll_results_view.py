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
        self.user = User.objects.get(username='johndoe')
        self.poll = Poll.objects.create(title='Poll 1', user=self.user, status='active', number_code=111111)
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

    def test_submit_match_question_response(self):
        self.client.force_login(self.user)
        response = self.client.post(self.poll_results_url, {
            'match_responses': json.dumps({'key1': 'value1'})
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue(MatchQuestionResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_match).exists())

    def test_submit_multiple_choice_response(self):
        self.client.force_login(self.user)
        response = self.client.post(self.poll_results_url, {
            'multiple_choice_responses': json.dumps(['option1', 'option2'])
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MultipleChoiceResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_multiple).exists())
    
    def test_submit_single_choice_response(self):
        self.client.force_login(self.user)
        response = self.client.post(self.poll_results_url, {
            'single_choice_response': 'option1'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SingleChoiceResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_single).exists())
    
    def test_submit_dropdown_fill_response(self):
        self.client.force_login(self.user)
        response = self.client.post(self.poll_results_url, {
            'dropdown_response': 'dropdown_option1'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(DropdownFillResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_dropdown).exists())
    
    def test_submit_text_fill_response(self):
        self.client.force_login(self.user)
        response = self.client.post(self.poll_results_url, {
            'text_fill_response': 'Sample Answer'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TextFillResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_text).exists())
    
    def test_submit_wordcloud_response(self):
        self.client.force_login(self.user)
        response = self.client.post(self.poll_results_url, {
            'word_cloud_responses': json.dumps(['word1', 'word2'])
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(WordCloudResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_wordcloud).exists())

    def test_submit_empty_wordcloud_response(self):
        self.client.force_login(self.user)
        response = self.client.post(self.poll_results_url, {
            'word_cloud_responses': json.dumps([])
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(WordCloudResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_wordcloud).exists())

    def test_submit_invalid_json_response(self):
        self.client.force_login(self.user)
        response = self.client.post(self.poll_results_url, {
            'match_responses': 'invalid json'
        })
        self.assertEqual(response.status_code, 400)

    def test_submit_no_data_response(self):
        self.client.force_login(self.user)
        response = self.client.post(self.poll_results_url, {})
        self.assertEqual(response.status_code, 302)  # Assuming redirect to the results page
        self.assertFalse(MatchQuestionResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_match).exists())
        self.assertFalse(MultipleChoiceResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_multiple).exists())
        self.assertFalse(SingleChoiceResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_single).exists())
        self.assertFalse(DropdownFillResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_dropdown).exists())
        self.assertFalse(TextFillResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_text).exists())
        self.assertFalse(WordCloudResponse.objects.filter(user=self.user, poll=self.poll, question=self.question_wordcloud).exists())

