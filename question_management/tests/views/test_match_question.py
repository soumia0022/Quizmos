from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll

class MatchQuestionTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a sample poll
        self.poll = Poll.objects.create(
            title="Sample Poll",
        )

        # Set the URL for the view handling question creation
        self.create_question_url = reverse('question_management:add_question', kwargs={'poll_id': self.poll.id})

    def test_match_question_creation(self):
        """
        Test creating a match question with valid data.
        """
        data = {
            'question_type': 'match_question',
            'match_question': 'Match the items in column A with column B.',
            'match_question_options[]': ['A1', 'A2', 'A3'],
            'match_question_answers[]': ['B1', 'B2', 'B3']
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status
        self.assertEqual(response.status_code, 302)  # Assuming a redirect occurs after creation

        # Check that the question was created in the database
        question = Question.objects.get(question_type='match_question')
        self.assertEqual(question.poll_id, self.poll.id)
        self.assertEqual(question.question_text, data['match_question'])
        self.assertEqual(question.match_options, data['match_question_options[]'])
        self.assertEqual(question.match_answers, data['match_question_answers[]'])

    def test_invalid_match_question_no_options(self):
        """
        Test creating a match question with missing options.
        """
        data = {
            'question_type': 'match_question',
            'match_question': 'Match the items in column A with column B.',
            'match_question_options[]': [],  # No options
            'match_question_answers[]': ['B1', 'B2', 'B3']
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('At least one option is required', response.json().get('error'))

    def test_invalid_match_question_no_answers(self):
        """
        Test creating a match question with missing answers.
        """
        data = {
            'question_type': 'match_question',
            'match_question': 'Match the items in column A with column B.',
            'match_question_options[]': ['A1', 'A2', 'A3'],
            'match_question_answers[]': []  # No answers
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('At least one answer is required', response.json().get('error'))

    def test_invalid_match_question_no_data(self):
        """
        Test creating a match question with no options or answers.
        """
        data = {
            'question_type': 'match_question',
            'match_question': '',
            'match_question_options[]': [],
            'match_question_answers[]': []
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('At least one option is required', response.json().get('error'))
