from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class EditCodeQuestionTestCase(TestCase):
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

        # Create a test coding question
        self.question = Question.objects.create(
            poll=self.poll,
            question_text="Original Coding Question?",
            question_type="code_question",
            code_question_text="Write a function to add two numbers.",
            code_language="python",
            correct_code="def add(a, b): return a + b",
            question_timer=60
        )

        # Define URL
        self.edit_question_url = reverse('question_management:edit_question', kwargs={'poll_id': self.poll.id})

    def test_edit_code_question_success(self):
        """
        Test successfully updating a coding question.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Coding Question?',
            'code_language': 'javascript',
            'correct_code': 'function add(a, b) { return a + b; }'
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect

        # Verify database update
        self.question.refresh_from_db()
        self.assertEqual(self.question.question_text, 'Updated Coding Question?')
        self.assertEqual(self.question.code_language, 'javascript')
        self.assertEqual(self.question.correct_code, 'function add(a, b) { return a + b; }')

    def test_edit_code_question_missing_question_text(self):
        """
        Test editing a coding question without providing question text.
        """
        data = {
            'question_id': self.question.id,
            'question_text': '',  # No question text provided
            'code_language': 'python',
            'correct_code': 'def add(a, b): return a + b'
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('Question text is required', response.json().get('error'))

    def test_edit_code_question_missing_language(self):
        """
        Test editing a coding question without selecting a language.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Coding Question?',
            'code_language': '',  # No language provided
            'correct_code': 'def add(a, b): return a + b'
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('Code language is required', response.json().get('error'))

    def test_edit_code_question_missing_correct_code(self):
        """
        Test editing a coding question without providing correct code.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Coding Question?',
            'code_language': 'python',
            'correct_code': ''  # No correct code provided
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('Correct code is required', response.json().get('error'))
