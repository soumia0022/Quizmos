from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class DeleteQuestionTestCase(TestCase):
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
        self.delete_question_url = reverse('question_management:delete_question', kwargs={'poll_id': self.poll.id})

    def test_delete_question_success(self):
        """
        Test successfully deleting a question.
        """
        response = self.client.get(self.delete_question_url + f"?question_id={self.question.id}")

        self.assertEqual(response.status_code, 302)

        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=self.question.id)

    def test_delete_non_existent_question(self):
        """
        Test deleting a non-existent question.
        """
        response = self.client.get(self.delete_question_url + "?question_id=9999")

        self.assertEqual(response.status_code, 404)
