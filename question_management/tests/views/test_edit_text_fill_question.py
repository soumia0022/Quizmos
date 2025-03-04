from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class EditTextFillQuestionTestCase(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.client = Client()
        self.client.login(username='johndoe', password='Password123')

        # Create a sample poll
        self.poll = Poll.objects.create(
            title="Sample Poll",
            user=User.objects.get(username='johndoe'),
        )

        # Create a test text-fill question
        self.question = Question.objects.create(
            poll=self.poll,
            question_text="Original Text Fill Question",
            question_type="text_fill",
            text_fill_question="Original Text Fill Question",
            text_fill_answer="OriginalAnswer",
            question_timer=30
        )

        # Define URL
        self.edit_question_url = reverse('question_management:edit_question', kwargs={'poll_id': self.poll.id})

    def test_edit_text_fill_question_success(self):
        """
        Test successfully updating a text-fill question.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Text Fill Question?',
            'text_fill_answer': 'UpdatedAnswer'
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 302)  # Redirect expected

        # Verify database update
        self.question.refresh_from_db()
        self.assertEqual(self.question.text_fill_question, 'Updated Text Fill Question?')
        self.assertEqual(self.question.text_fill_answer, 'UpdatedAnswer')

    def test_edit_text_fill_question_missing_question_text(self):
        """
        Test editing a text-fill question without providing question text.
        """
        data = {
            'question_id': self.question.id,
            'question_text': '',  # No question text provided
            'text_fill_answer': 'UpdatedAnswer'
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        # Assuming you return a 400 error for missing question text
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('Question text is required', response.json().get('error'))

    def test_edit_text_fill_question_missing_answer(self):
        """
        Test editing a text-fill question without providing an answer.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Text Fill Question?',
            'text_fill_answer': ''  # No answer provided
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        # Assuming you return a 400 error for missing answer
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('Text fill answer is required', response.json().get('error'))
