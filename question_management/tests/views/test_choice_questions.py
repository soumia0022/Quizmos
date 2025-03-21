from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User

class QuestionTypesTestCase(TestCase):
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

        # Set the URL for the view handling question creation
        self.create_question_url = reverse('question_management:add_question', kwargs={'poll_id': self.poll.id})

    def test_multiple_choice_question_creation(self):
        data = {
            'question_type': 'multiple_choice',
            'multiple_choice_question': 'What are your favorite fruits?',
            'multiple_choice_options[]': ['Apple', 'Banana', 'Cherry'],
            'multiple_choice_answers[]': ['Apple', 'Cherry']
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status
        self.assertEqual(response.status_code, 302)  # Assuming a redirect occurs after creation

        # Check that the question was created in the database
        question = Question.objects.get(question_type='multiple_choice')
        self.assertEqual(question.poll_id, self.poll.id)
        self.assertEqual(question.question_text, data['multiple_choice_question'])
        self.assertEqual(question.multiple_choice_options, data['multiple_choice_options[]'])
        self.assertEqual(question.multiple_choice_answers, data['multiple_choice_answers[]'])

    def test_single_choice_question_creation(self):
        """
        Test creating a single-choice question with valid data.
        """
        data = {
            'question_type': 'single_choice',
            'single_choice_question': 'What is your favorite color?',
            'single_choice_options[]': ['Red', 'Blue', 'Green'],
            'single_choice_answers[]': ['Blue']
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status
        self.assertEqual(response.status_code, 302)

        # Check that the question was created in the database
        question = Question.objects.get(question_type='single_choice')
        self.assertEqual(question.poll_id, self.poll.id)
        self.assertEqual(question.question_text, data['single_choice_question'])
        self.assertEqual(question.single_choice_option, data['single_choice_options[]'])
        self.assertEqual(question.single_choice_answers, data['single_choice_answers[]'])

    def test_invalid_multiple_choice_question(self):
        # Missing options and answers
        data = {
            'question_type': 'multiple_choice',
            'multiple_choice_question': 'What is 2 + 2?',
            'multiple_choice_options[]': [],  # No options
            'multiple_choice_answers[]': []  # No answers
        }
        response = self.client.post(self.create_question_url, data)

        # Ensure it returns a 400 status with an error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('At least one option is required', response.json().get('error'))

    def test_invalid_multiple_choice_question_with_no_answers(self):
        # Missing options and answers
        data = {
            'question_type': 'multiple_choice',
            'multiple_choice_question': 'What is 2 + 2?',
            'multiple_choice_options[]': ["Option1"],  # No options
            'multiple_choice_answers[]': []  # No answers
        }
        response = self.client.post(self.create_question_url, data)

        # Ensure it returns a 400 status with an error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('At least one answer is required', response.json().get('error'))

    def test_invalid_single_choice_question(self):
        """
        Test creating a single-choice question with missing options or answers.
        """
        data = {
            'question_type': 'single_choice',
            'single_choice_question': 'What is your favorite color?',
            'single_choice_options[]': [],
            'single_choice_answers[]': []
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status
        # Ensure it returns a 400 status with an error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('At least one option is required', response.json().get('error'))

    def test_invalid_single_choice_question_with_no_answer(self):
        """
        Test creating a single-choice question with missing options or answers.
        """
        data = {
            'question_type': 'single_choice',
            'single_choice_question': 'What is your favorite color?',
            'single_choice_options[]': ["Option1"],
            'single_choice_answers[]': []
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status
        # Ensure it returns a 400 status with an error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('At least one answer is required', response.json().get('error'))

    def test_exceeding_option_limit_multiple_choice(self):
        """
        Test that adding more than 4 options to a multiple-choice question results in an error.
        """
        data = {
            'question_type': 'multiple_choice',
            'multiple_choice_question': 'Select all prime numbers.',
            'multiple_choice_options[]': ['2', '3', '5', '7', '11'],  # 5 options (exceeds limit)
            'multiple_choice_answers[]': ['2', '3']
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Ensure it returns a 400 status with the correct error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('You can only add up to 4 options for a multiple_choice question.', response.json().get('error'))

    def test_exceeding_option_limit_single_choice(self):
        """
        Test that adding more than 4 options to a single-choice question results in an error.
        """
        data = {
            'question_type': 'single_choice',
            'single_choice_question': 'What is the capital of France?',
            'single_choice_options[]': ['Paris', 'London', 'Berlin', 'Madrid', 'Rome'],  # 5 options (exceeds limit)
            'single_choice_answers[]': ['Paris']
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Ensure it returns a 400 status with the correct error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('You can only add up to 4 options for a single_choice question.', response.json().get('error'))
