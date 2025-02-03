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
            multiple_choice_options=['Option1', 'Option2'],
            multiple_choice_answers=['Option1'],
            timer=30
        )

        # Define URL
        self.edit_question_url = reverse('question_management:edit_question', kwargs={'poll_id': self.poll.id})

    def test_edit_question_success(self):
        """
        Test successfully editing a question.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Question?',
            'question_timer': '45',
            'multiple_choice_options[]': ['Updated Option1', 'Updated Option2'],
            'multiple_choice_answers[]': ['Updated Option1']
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 302)

        # Check if the question is updated in the database
        self.question.refresh_from_db()
        self.assertEqual(self.question.question_text, 'Updated Question?')
        self.assertEqual(self.question.timer, 45)
        self.assertEqual(self.question.multiple_choice_options, ['Updated Option1', 'Updated Option2'])
        self.assertEqual(self.question.multiple_choice_answers, ['Updated Option1'])

    def test_edit_question_missing_fields(self):
        """
        Test editing a question with missing required fields.
        """
        data = {
            'question_id': self.question.id,
            'question_text': '',
            'question_timer': '45'
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_edit_single_choice_question(self):
        """
        Test editing a single-choice question.
        """
        self.question.question_type = 'single_choice'
        self.question.save()

        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Single Choice?',
            'question_timer': '60',
            'single_choice_options[]': ['OptionA', 'OptionB'],
            'single_choice_answers[]': 'OptionA'
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 302)

        self.question.refresh_from_db()
        self.assertEqual(self.question.question_text, 'Updated Single Choice?')
        self.assertEqual(self.question.timer, 60)
        self.assertEqual(self.question.single_choice_option, ['OptionA', 'OptionB'])
        self.assertEqual(self.question.single_choice_answers, ['OptionA'])
