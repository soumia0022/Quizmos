from django.test import TestCase, Client
from django.urls import reverse
from io import StringIO
import csv
from user_management.models import User
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question
from response_management.models.response_model import (
    MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse,
    DropdownFillResponse, MatchQuestionResponse
)


class CSVDownloadTestCase(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        """Set up test data for polls, questions, and responses."""
        self.client = Client()
        self.user = User.objects.get(username='johndoe')
        self.user.set_password('password')
        self.user.save()
        self.client.login(username='johndoe', password='password')

        self.poll = Poll.objects.create(title="Sample Poll", user=self.user)

        # Create different types of questions

        self.multiple_choice_question = Question.objects.create(
            poll=self.poll,
            question_text="Favorite Color?",
            question_type="multiple_choice",
            multiple_choice_options=["Red", "Blue", "Green"],
            multiple_choice_answers = ["Red"]
        )

        self.single_choice_question = Question.objects.create(
            poll=self.poll,
            question_text="Best Programming Language?",
            question_type="single_choice",
            single_choice_option=["Python", "Java", "C++"]
        )

        self.text_fill_question = Question.objects.create(
            poll=self.poll,
            question_text="Describe your experience?",
            question_type="text_fill"
        )

        self.dropdown_question = Question.objects.create(
            poll=self.poll,
            question_text="Select your country?",
            question_type="dropdown_fill",
            dropdown_options=["USA", "UK", "India"]
        )

        self.match_question = Question.objects.create(
            poll=self.poll,
            question_type="match_question",
            match_question="Match the countries to their capitals.",
            match_options=["France", "Germany", "Italy"],
            match_answers=["Paris", "Berlin", "Rome"],
            question_text="Match the countries to their capitals.",
        )

        # Create responses

        MultipleChoiceResponse.objects.create(
            poll=self.poll,
            question=self.multiple_choice_question,
            user=self.user,
            selected_options=["Red"]
        )

        SingleChoiceResponse.objects.create(
            poll=self.poll,
            question=self.single_choice_question,
            user=self.user,
            selected_option="Python"
        )

        TextFillResponse.objects.create(
            poll=self.poll,
            question=self.text_fill_question,
            user=self.user,
            answer_text="Great!"
        )

        DropdownFillResponse.objects.create(
            poll=self.poll,
            question=self.dropdown_question,
            user=self.user,
            selected_option="USA"
        )

        MatchQuestionResponse.objects.create(
            poll=self.poll,
            question=self.match_question,
            user=self.user,
            match_responses=[
                {"France": "Paris"},
                {"Germany": "Berlin"},
                {"Italy": "Rome"}
            ]
        )

    def test_download_csv_valid_poll(self):
        """Test CSV download for a valid poll with responses."""
        url = reverse("download_csv", args=[self.poll.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertTrue('Content-Disposition' in response)
        self.assertIn(f'attachment; filename="{self.poll.title}_responses.csv"', response['Content-Disposition'])

        # Read the CSV data
        csv_data = StringIO(response.content.decode('utf-8'))
        reader = csv.reader(csv_data)

        # Check the CSV headers
        headers = next(reader)
        self.assertEqual(headers,['User', 'Question', 'Question Type', 'Options', 'Correct Answer', 'Number of Responses'])

        # Check the rows in the CSV
        rows = list(reader)
        self.assertEqual(len(rows), 5)  # 5 questions in the poll in total

        # Check specific question response data (e.g., for multiple choice question)
        row = rows[0]
        self.assertEqual(row[0], self.user.username)
        self.assertEqual(row[1], "Favorite Color?")
        self.assertEqual(row[2], "Multiple Choice")
        self.assertEqual(row[3], "Red, Blue, Green")
        self.assertEqual(row[4], "Red")
        self.assertEqual(row[5], "1")

    def test_download_csv_invalid_poll(self):
        """Test CSV download for an invalid poll (non-existent poll)."""
        url = reverse("download_csv", args=[99999]) # Poll ID does not exist
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
