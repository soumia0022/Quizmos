from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class EditSingleChoiceQuestionTestCase(TestCase):
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
            question_text="Original Single Choice Question",
            question_type="single_choice",
            single_choice_question="Original Single Choice Question",
            single_choice_option=['Option1', 'Option2', 'Option3'],
            single_choice_answers=['Option1'],
            question_timer=30
        )

        # Define URL
        self.edit_question_url = reverse('question_management:edit_question', kwargs={'poll_id': self.poll.id})

    def test_edit_single_choice_question_success(self):
        """
        Test successfully updating a single-choice question.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Single Choice Question?',
            'single_choice_options[]': ['NewOption1', 'NewOption2', 'NewOption3'],
            'single_choice_answers[]': ['NewOption1']
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 302)  # Redirect expected

        # Verify database update
        self.question.refresh_from_db()
        self.assertEqual(self.question.question_text, 'Updated Single Choice Question?')
        self.assertEqual(self.question.single_choice_option, ['NewOption1', 'NewOption2', 'NewOption3'])
        self.assertEqual(self.question.single_choice_answers, ['NewOption1'])

    def test_edit_single_choice_question_missing_options(self):
        """
        Test editing a single-choice question with missing options.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Single Choice Question?',
            ' single_choice_options[]': [],  # No options provided
            'single_choice_answers[]': 'NewOption1'
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('At least one option is required', response.json().get('error'))

    def test_edit_single_choice_question_missing_answers(self):
        """
        Test editing a single-choice question with missing answers.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Single Choice Question?',
            'single_choice_options[]': ['NewOption1', 'NewOption2', 'NewOption3'],
            'single_choice_answers[]': ''  # No answer provided
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data,
                                    content_type='application/x-www-form-urlencoded')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('At least one answer is required', response.json().get('error'))

    def test_edit_single_choice_question_multiple_answers(self):
        """
        Test editing a single-choice question with multiple answers (invalid case).
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Single Choice Question?',
            ' single_choice_options': ['NewOption1', 'NewOption2'],
            'single_choice_answers[]': ['NewOption1', 'NewOption2']  # Multiple answers (invalid)
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data,
                                    content_type='application/x-www-form-urlencoded')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('At least one answer is required for a single-choice question', response.json().get('error'))

    def test_edit_single_choice_question_no_changes(self):
        """
        Test editing a single-choice question without making any changes.
        """
        data = {
            'question_id': self.question.id,
            'question_text': self.question.question_text,
            ' single_choice_options': self.question.single_choice_option,
            'single_choice_answers[]': self.question.single_choice_answers
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 400)  # Should still redirect

        # Verify no change in the database
        self.question.refresh_from_db()
        self.assertEqual(self.question.question_text, "Original Single Choice Question")
        self.assertEqual(self.question.single_choice_option, ['Option1', 'Option2', 'Option3'])
        self.assertEqual(self.question.single_choice_answers, ['Option1'])

    def test_edit_single_choice_question_exceeding_option_limit(self):
        """
        Test that editing a single-choice question to have more than 4 options results in an error.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Single Choice Question?',
            'single_choice_options[]': ['Option1', 'Option2', 'Option3', 'Option4', 'Option5'],  # 5 options (exceeds limit)
            'single_choice_answers[]': ['Option1']
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        # Ensure it returns a 400 status with the correct error message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('You can only add up to 4 options for a single-choice question.', response.json().get('error'))

