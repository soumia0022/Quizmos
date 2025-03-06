from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class EditMatchQuestionTestCase(TestCase):
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

        # Create a test match question
        self.question = Question.objects.create(
            poll=self.poll,
            question_text="Original Match Question",
            question_type="match_question",
            match_question="Original Match Question",
            match_options=['Option1', 'Option2', 'Option3'],
            match_answers=['Answer1', 'Answer2', 'Answer3'],
            question_timer=30
        )

        # Define URL
        self.edit_question_url = reverse('question_management:edit_question', kwargs={'poll_id': self.poll.id})

    def test_edit_match_question_success(self):
        """
        Test successfully updating a match question.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Match Question?',  # Updated question text
            'match_question_options[]': ['NewOption1', 'NewOption2', 'NewOption3'],
            'match_question_answers[]': ['NewAnswer1', 'NewAnswer2', 'NewAnswer3']  # Correct answers
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 302)  # Redirect expected

        # Verify database update
        self.question.refresh_from_db()
        self.assertEqual(self.question.match_question, 'Updated Match Question?')
        self.assertEqual(self.question.match_options, ['NewOption1', 'NewOption2', 'NewOption3'])
        self.assertEqual(self.question.match_answers, ['NewAnswer1', 'NewAnswer2', 'NewAnswer3'])

    def test_edit_match_question_missing_options(self):
        """
        Test editing a match question with missing options.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Match Question?',
            'match_question_options[]': [],  # No options provided
            'match_question_answers[]': ['NewAnswer1']
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        # Expect an error for missing options
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('At least one option is required for a match question.', response.json().get('error'))

    def test_edit_match_question_missing_answers(self):
        """
        Test editing a match question with missing answers.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Match Question?',
            'match_question_options[]': ['NewOption1'],
            'match_question_answers[]': []  # No answers provided
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        # Expect an error for missing answers
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('At least one answer is required for a match question.', response.json().get('error'))

    def test_edit_match_question_options_and_answers_mismatch(self):
        """
        Test editing a match question with mismatched number of options and answers.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Match Question?',
            'match_question_options[]': ['NewOption1', 'NewOption2'],
            'match_question_answers[]': ['NewAnswer1']  # Mismatch in the number of answers
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        # Expect an error for mismatched number of options and answers
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('The number of options must match the number of answers.', response.json().get('error'))
