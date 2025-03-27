from django.test import TestCase
from django.urls import reverse
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question
from user_management.models import User

class DisplayCodeViewTest(TestCase):
     
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]
     
    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.poll = Poll.objects.create(title = 'test_poll', user=self.user)


    def test_display_code_with_empty_poll(self):
        url = reverse('poll_management:display_code', args=[self.poll.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)


    def test_display_code(self):
        self.mcq_question = Question.objects.create(
            poll=self.poll,
            question_type='multiple_choice',
            multiple_choice_question='What is the capital of France?',
            multiple_choice_options=['Paris', 'London', 'Berlin', 'Madrid'],
            multiple_choice_answers=['Paris']
        )
        url = reverse('poll_management:display_code', args=[self.poll.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.poll.title)
        self.assertTemplateUsed(response, 'display_code.html')

        self.assertIn('qrcode', response.context)