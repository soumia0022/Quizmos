from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class EditDropdownFillQuestionTestCase(TestCase):
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

        # Create a test dropdown-fill question
        self.question = Question.objects.create(
            poll=self.poll,
            question_text="Original Dropdown Fill Question",
            question_type="dropdown_fill",
            dropdown_options="Option1,Option2,Option3",
            dropdown_correct_answer="Option1",
            question_timer=30
        )

        # Define URL
        self.edit_question_url = reverse('question_management:edit_question', kwargs={'poll_id': self.poll.id})

    def test_edit_dropdown_fill_question_success(self):
        """
        Test successfully updating a dropdown-fill question.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Dropdown Fill Question?',
            'dropdown_options[]': ['NewOption1', 'NewOption2', 'NewOption3'],
            'dropdown_correct_answer': 'NewOption2'
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 302)  # Redirect expected

        # Verify database update
        self.question.refresh_from_db()
        self.assertEqual(self.question.dropdown_options, "NewOption1,NewOption2,NewOption3")
        self.assertEqual(self.question.dropdown_correct_answer, "NewOption2")

    def test_edit_dropdown_fill_question_missing_options(self):
        """
        Test editing a dropdown-fill question without providing dropdown options.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Dropdown Fill Question?',
            'dropdown_options[]': [],  # No options provided
            'dropdown_correct_answer': 'NewOption1'
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        # Assuming you return a 400 error for missing options
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('At least one option is required', response.json().get('error'))

    def test_edit_dropdown_fill_question_missing_correct_answer(self):
        """
        Test editing a dropdown-fill question without providing a correct answer.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated Dropdown Fill Question?',
            'dropdown_options[]': ['NewOption1', 'NewOption2'],
            'dropdown_correct_answer': ''  # No correct answer provided
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        # Assuming you return a 400 error for missing correct answer
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('A correct answer is required', response.json().get('error'))
