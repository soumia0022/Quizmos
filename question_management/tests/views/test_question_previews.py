from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models import User

class QuestionPreviewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.poll = Poll.objects.create(title="Test Poll", user=self.user)
        self.question = Question.objects.create(
            poll=self.poll,
            question_type='multiple_choice',
            timer=30,
            question_text="What is your favorite color?",
        )

    def test_question_preview_view(self):
        response = self.client.get(reverse('question_management:question_preview', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'question_type': self.question.get_question_type_display(),
            'timer': self.question.timer,
            'question_text': self.question.question_text,
        })

class QuestionDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.poll = Poll.objects.create(title="Test Poll", user=self.user)
        self.question = Question.objects.create(
            poll=self.poll,
            question_type='multiple_choice',
            timer=30,
            question_text="What is your favorite color?",
        )

    def test_question_detail_view(self):
        response = self.client.get(reverse('question_management:question_detail', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'question_detail.html')
        self.assertContains(response, self.question.question_text)
        context_timer = response.context['question'].timer
        self.assertEqual(context_timer, 30)
