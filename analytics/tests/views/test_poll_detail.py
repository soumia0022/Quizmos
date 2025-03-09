from django.test import TestCase, Client
from django.urls import reverse

from user_management.models import User
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question
from response_management.models.response_model import MultipleChoiceResponse, SingleChoiceResponse, TextFillResponse, DropdownFillResponse, MatchQuestionResponse

# Will add tests for wordcloud and code question once functionality has been added
# Will add tests when other analytics have been completed - correct/incorrect answers


class PollAnalyticsTestCase(TestCase):
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
            question_text="Favorite Colour?",
            question_type="multiple_choice",
            multiple_choice_options=["Red", "Blue", "Green"]
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

    def test_poll_analytics_view(self):
        """Test that the poll analytics page loads correctly."""
        url = reverse("poll_analytics", args=[self.poll.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "poll_detail.html")

    def test_pie_chart_poll_view(self):
        """Test pie chart data returns correct labels and response counts."""
        url = reverse("piechart_data", args=[self.poll.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200, "Graph data view did not return a 200 status code")
        self.assertTrue(response.headers.get("Content-Type", "").startswith("application/json"),
                        f"Expected JSON response but got: {response.headers.get('Content-Type')}") # Ensure JSON response
        json_response = response.json()
        self.assertEqual(set(json_response.keys()), {"labels", "data"})
        expected_labels = ["Favorite Colour?", "Best Programming Language?", "Describe your experience?", "Select your country?", "Match the countries to their capitals."]
        self.assertListEqual(json_response["labels"], expected_labels)
        self.assertEqual(json_response["data"], [1, 1, 1, 1, 1])  # One response per question

    def test_bar_graph_poll_view(self):
        """Test bar graph data returns correct labels and response counts."""
        url = reverse("bargraph_data", args=[self.poll.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200, "Graph data view did not return a 200 status code")
        self.assertTrue(response.headers.get("Content-Type", "").startswith("application/json"),
                        f"Expected JSON response but got: {response.headers.get('Content-Type')}")  # Ensure JSON response
        json_response = response.json()
        self.assertEqual(set(json_response.keys()), {"labels", "data"})
        expected_labels = ["Favorite Colour?", "Best Programming Language?", "Describe your experience?",
                           "Select your country?", "Match the countries to their capitals."]
        self.assertListEqual(json_response["labels"], expected_labels)
        self.assertEqual(json_response["data"], [1, 1, 1, 1, 1])  # One response per question

    def test_line_graph_poll_view(self):
        """Test line graph data returns correct labels and response counts."""
        url = reverse("linegraph_data", args=[self.poll.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200, "Graph data view did not return a 200 status code")
        self.assertTrue(response.headers.get("Content-Type", "").startswith("application/json"),
                        f"Expected JSON response but got: {response.headers.get('Content-Type')}")  # Ensure JSON response
        json_response = response.json()
        self.assertEqual(set(json_response.keys()), {"labels", "data"})
        expected_labels = ["Favorite Colour?", "Best Programming Language?", "Describe your experience?",
                           "Select your country?", "Match the countries to their capitals."]
        self.assertListEqual(json_response["labels"], expected_labels)
        self.assertEqual(json_response["data"], [1, 1, 1, 1, 1])  # One response per question

    def test_multiple_choice_question_analytics(self):
        """Test analytics for multiple-choice questions."""
        url = reverse("question_analytics", args=[self.multiple_choice_question.id])
        response = self.client.get(url)
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["question"], "Favorite Colour?")
        self.assertListEqual(json_response["labels"], ["Red", "Blue", "Green"])
        self.assertListEqual(json_response["data"], [1, 0, 0])  # "Red" has 1 response

    def test_single_choice_question_analytics(self):
        """Test analytics for single-choice questions."""
        url = reverse("question_analytics", args=[self.single_choice_question.id])
        response = self.client.get(url)
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["question"], "Best Programming Language?")
        self.assertListEqual(json_response["labels"], ["Python", "Java", "C++"])
        self.assertListEqual(json_response["data"], [1, 0, 0])  # "Python" has 1 response

    def test_text_fill_question_analytics(self):
        """Test analytics for text-fill responses."""
        url = reverse("question_analytics", args=[self.text_fill_question.id])
        response = self.client.get(url)
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["question"], "Describe your experience?")
        self.assertListEqual(json_response["labels"], ["Great!"])
        self.assertListEqual(json_response["data"], [1])

    def test_dropdown_question_analytics(self):
        """Test analytics for dropdown-fill responses."""
        url = reverse("question_analytics", args=[self.dropdown_question.id])
        response = self.client.get(url)
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["question"], "Select your country?")

    def test_match_question_analytics(self):
        """Test analytics for match question responses."""
        url = reverse("question_analytics", args=[self.match_question.id])
        response = self.client.get(url)
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["question"], "Match the countries to their capitals.")
        self.assertListEqual(json_response["labels"], ["Total Number of Matches"])
        self.assertListEqual(json_response["data"], [1])  # One response