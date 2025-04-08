from django.http import JsonResponse
from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from question_management.views.edit_question_manager import QuestionManager
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
            question_timer=30
        )

        self.scq_question = Question.objects.create(
            question_text="Single Choice Question",
            question_type="single_choice",
            single_choice_option=['Option1', 'Option2'],
            single_choice_answers=['Option1', 'Option2'],  # This simulates the error (multiple answers)
            question_timer=30
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
        self.assertEqual(self.question.question_timer, 45)
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
        self.assertEqual(self.question.question_timer, 60)
        self.assertEqual(self.question.single_choice_option, ['OptionA', 'OptionB'])
        self.assertEqual(self.question.single_choice_answers, ['OptionA'])

    def test_edit_question_view_success(self):
        """
        Test if the edit question page loads successfully with a valid poll and question.
        """
        url = self.edit_question_url + f'?question_id={self.question.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_question.html')
        self.assertIn('question', response.context)
        self.assertEqual(response.context['question'].question_text, "Original Question")

    def test_edit_question_view_404_invalid_poll(self):
        """
        Test if the view returns 404 when the poll does not exist.
        """
        url = reverse('question_management:edit_question', kwargs={'poll_id': 999}) + f'?question_id={self.question.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_edit_question_view_404_invalid_question(self):
        """
        Test if the view returns 404 when the question does not exist.
        """
        url = self.edit_question_url + '?question_id=999'  # Invalid question ID
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_edit_question_view_match_pairs(self):
        """
        Test if the match pairs are zipped correctly in the context.
        """
        self.question.match_options = ['A', 'B', 'C']
        self.question.match_answers = ['1', '2', '3']
        self.question.save()

        url = self.edit_question_url + f'?question_id={self.question.id}'
        response = self.client.get(url)

        expected_match_pairs = list(zip(["A", "B", "C"], ["1", "2", "3"]))
        self.assertEqual(list(response.context['match_pairs']), expected_match_pairs)

    def test_validate_single_choice_multiple_answers(self):
        """Test that the validation catches multiple answers for a single-choice question."""
        validation_response = QuestionManager.validate_single_choice(self.scq_question)
        self.assertIsInstance(validation_response, JsonResponse)
        self.assertEqual(validation_response.status_code, 400)
