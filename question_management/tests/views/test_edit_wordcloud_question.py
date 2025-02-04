from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class EditWordCloudQuestionTestCase(TestCase):
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

        # Create a test wordcloud question
        self.question = Question.objects.create(
            poll=self.poll,
            question_text="Original WordCloud Question",
            question_type="wordcloud",
            wordcloud_question="Original WordCloud Question",
            timer=30
        )

        # Define URL
        self.edit_question_url = reverse('question_management:edit_question', kwargs={'poll_id': self.poll.id})

    def test_edit_wordcloud_question_success(self):
        """
        Test successfully updating a wordcloud question.
        """
        data = {
            'question_id': self.question.id,
            'question_text': 'Updated WordCloud Question?'  # Updated question text
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        self.assertEqual(response.status_code, 302)  # Redirect expected

        # Verify database update
        self.question.refresh_from_db()
        self.assertEqual(self.question.wordcloud_question, 'Updated WordCloud Question?')

    def test_edit_wordcloud_question_missing_text(self):
        """
        Test editing a wordcloud question with missing question text.
        """
        data = {
            'question_id': self.question.id,
            'question_text': ''  # No question text provided
        }

        response = self.client.post(self.edit_question_url + f"?question_id={self.question.id}", data)

        # Expect an error for missing text
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn('Question text is required for a wordcloud question.', response.json().get('error'))
