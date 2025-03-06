from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models import User

class QuestionListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.poll = Poll.objects.create(title="Test Poll", user=self.user)
        self.question1 = Question.objects.create(
            poll=self.poll,
            question_type='multiple_choice',
            question_timer=30,
            question_text="What is your favorite color?",
        )
        self.question2 = Question.objects.create(
            poll=self.poll,
            question_type='text',
            question_timer=45,
            question_text="Describe your favorite hobby."
        )

    def test_question_list_view(self):
        response = self.client.get(reverse('question_management:question_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'question_list.html')
        self.assertContains(response, "What is your favorite color?")
        self.assertContains(response, "Describe your favorite hobby.")
