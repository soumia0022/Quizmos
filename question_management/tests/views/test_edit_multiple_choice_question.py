from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class EditQuestionTestCase(TestCase):
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

        # Create a test question
        self.question = Question.objects.create(
            poll=self.poll,
            question_text="Original Question",
            question_type="multiple_choice",
            multiple_choice_question="Original Question",
            multiple_choice_options=['Option1', 'Option2'],
            multiple_choice_answers=['Option1'],
            timer=30
        )

        # Define URL
        self.edit_question_url = reverse('question_management:edit_question', kwargs={'poll_id': self.poll.id})

    def test_edit_multiple_choice_question_success(self):
        """
        Test successfully updating a multiple-choice question.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Question?',
            'multiple_choice_options[]': ['NewOption1', 'NewOption2', 'NewOption3'],
            'multiple_choice_answers[]': ['NewOption1']
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 302)  # Redirect expected

        # Verify database update
        self.question.refresh_from_db()
        self.assertEqual(self.question.question_text, 'Updated Question?')
        self.assertEqual(self.question.multiple_choice_options, ['NewOption1', 'NewOption2', 'NewOption3'])
        self.assertEqual(self.question.multiple_choice_answers, ['NewOption1'])

    def test_edit_multiple_choice_question_missing_options(self):
        """
        Test editing a multiple-choice question with missing options.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Question?',
            'multiple_choice_options[]': [],  # No options provided
            'multiple_choice_answers[]': ['NewOption1']
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('At least one option is required', response.json().get('error'))

    def test_edit_multiple_choice_question_missing_answers(self):
        """
        Test editing a multiple-choice question with missing answers.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Question?',
            'multiple_choice_options[]': ['NewOption1', 'NewOption2'],
            'multiple_choice_answers[]': []  # No answers provided
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('At least one answer is required', response.json().get('error'))

    def test_edit_multiple_choice_question_no_changes(self):
        """
        Test editing a multiple-choice question without making any changes.
        """
        data = {
            'question_id': self.question.id,
            'question_text': self.question.question_text,
            'multiple_choice_options[]': self.question.multiple_choice_options,
            'multiple_choice_answers[]': self.question.multiple_choice_answers
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 302)  # Should still redirect

        # Verify no change in the database
        self.question.refresh_from_db()
        self.assertEqual(self.question.question_text, "Original Question")
        self.assertEqual(self.question.multiple_choice_options, ['Option1', 'Option2'])
        self.assertEqual(self.question.multiple_choice_answers, ['Option1'])
