from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models import User
import json

class CodeQuestionTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser",
            first_name="John",
            last_name="Doe",
            email="testuser@example.com",
            password="Password123",
            role="Lecturer",  # Specify role as required
        )
        self.client.login(username='testuser', password='Password123')

        # Create a sample poll
        self.poll = Poll.objects.create(
            title="Sample Poll",
            status="active",  # Setting default status
            user=self.user,  # Linking to the created user
            locked=False  # Default locked state
        )

        # Set the URL for the view handling question creation
        self.create_question_url = reverse('question_management:add_question', kwargs={'poll_id': self.poll.id})

    def test_poll_creation(self):
        # Ensure the poll was created correctly
        self.assertEqual(self.poll.title, "Sample Poll")
        self.assertEqual(self.poll.status, "active")
        self.assertFalse(self.poll.locked)
        self.assertEqual(self.poll.user, self.user)

    def test_code_question_creation(self):
        """
        Test creating a code question with valid data.
        """
        data = {
            'question_type': 'code_question',
            'code_question_text': 'Write a function to reverse a string.',
            'code_language': 'python',
            'code_test_cases': json.dumps([
                {"input": "hello", "output": "olleh"},
                {"input": "world", "output": "dlrow"}
            ])
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status
        self.assertEqual(response.status_code, 302)  # Assuming a redirect occurs after creation

        # Check that the question was created in the database
        question = Question.objects.get(question_type='code_question')
        self.assertEqual(question.poll_id, self.poll.id)
        self.assertEqual(question.code_question_text, data['code_question_text'])
        self.assertEqual(question.code_language, data['code_language'])
        self.assertEqual(question.code_test_cases, json.loads(data['code_test_cases']))

    def test_code_question_invalid_json_test_cases(self):
        """
        Test creating a code question with invalid JSON format for test cases.
        """
        data = {
            'question_type': 'code_question',
            'code_question_text': 'Write a function to reverse a string.',
            'code_language': 'python',
            'code_test_cases': '{"input": "hello", "output": "olleh" '  # Invalid JSON format
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid JSON format for test cases", response.json().get("error"))

    def test_code_question_missing_test_cases(self):
        """
        Test creating a code question with missing test cases.
        """
        data = {
            'question_type': 'code_question',
            'code_question_text': 'Write a function to reverse a string.',
            'code_language': 'python',
            'code_test_cases': '[]'  # Empty test cases
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status
        self.assertEqual(response.status_code, 302)  # Assuming a redirect occurs after creation
        question = Question.objects.get(question_type='code_question')
        self.assertEqual(question.poll_id, self.poll.id)
        self.assertEqual(question.code_test_cases, [])

    def test_code_question_missing_code_language(self):
        """
        Test creating a code question with missing code language.
        """
        data = {
            'question_type': 'code_question',
            'code_question_text': 'Write a function to reverse a string.',
            'code_language': '',  # Missing code language
            'code_test_cases': json.dumps([
                {"input": "hello", "output": "olleh"}
            ])
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status and error message
        self.assertEqual(response.status_code, 302)

    def test_code_question_missing_code_question_text(self):
        """
        Test creating a code question with missing question text.
        """
        data = {
            'question_type': 'code_question',
            'code_question_text': '',  # Missing code question text
            'code_language': 'python',
            'code_test_cases': json.dumps([
                {"input": "hello", "output": "olleh"}
            ])
        }

        # Send a POST request
        response = self.client.post(self.create_question_url, data)

        # Check response status and error message
        self.assertEqual(response.status_code, 302)
