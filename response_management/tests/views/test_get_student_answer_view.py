from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from response_management.models.response_model import (
    MultipleChoiceResponse, SingleChoiceResponse, DropdownFillResponse, TextFillResponse
)

class GetStudentAnswerViewTest(TestCase):

    def setUp(self):
        """Set up test data before each test"""
        User = get_user_model()
        self.student = User.objects.create_user(username="teststudent", password="testpass")

        # ✅ Fix: Assign a user when creating the Poll
        self.poll = Poll.objects.create(title="Test Poll", number_code=123456, user=self.student)

        # Create Questions with different types
        self.mcq_question = Question.objects.create(
            poll=self.poll,
            question_type="multiple_choice",
            question_text="What is 2 + 2?",
            multiple_choice_answers=["4"]
        )

        self.single_choice_question = Question.objects.create(
            poll=self.poll,
            question_type="single_choice",
            question_text="What is the capital of France?",
            single_choice_answers=["Paris"]
        )

        self.text_fill_question = Question.objects.create(
            poll=self.poll,
            question_type="text_fill",
            question_text="Complete the phrase: Hello, ____!",
            text_fill_answer="World"
        )

        self.dropdown_question = Question.objects.create(
            poll=self.poll,
            question_type="dropdown_fill",
            question_text="Choose the correct answer",
            dropdown_correct_answer="CorrectOption"
        )

        self.match_question = Question.objects.create(
            poll=self.poll,
            question_type="match_question",
            question_text="Match the following",
            match_answers={"A": "1", "B": "2"}
        )

        # Create Student Responses
        self.mcq_response = MultipleChoiceResponse.objects.create(
            user=self.student,
            poll=self.poll,
            question=self.mcq_question,
            selected_options=["4"]
        )

        self.single_choice_response = SingleChoiceResponse.objects.create(
            user=self.student,
            poll=self.poll,
            question=self.single_choice_question,
            selected_option="Paris"
        )

        self.text_fill_response = TextFillResponse.objects.create(
            user=self.student,
            poll=self.poll,
            question=self.text_fill_question,
            answer_text="World"
        )

        self.dropdown_response = DropdownFillResponse.objects.create(
            user=self.student,
            poll=self.poll,
            question=self.dropdown_question,
            selected_option="CorrectOption"
        )

    def test_api_returns_correct_answer_for_mcq(self):
        """Test if the API correctly returns MCQ correct answer"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, self.mcq_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["correct_answer"], ["4"])  # Correct answer
        self.assertEqual(data["selected_answer"], ["4"])  # Student's answer

    def test_api_returns_correct_answer_for_single_choice(self):
        """Test if the API correctly returns Single Choice correct answer"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, self.single_choice_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["correct_answer"], ["Paris"])  # Correct answer
        self.assertEqual(data["selected_answer"], "Paris")  # Student's answer

    def test_api_returns_correct_answer_for_text_fill(self):
        """Test if the API correctly returns Text Fill correct answer"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, self.text_fill_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["correct_answer"], "World")  # Correct answer
        self.assertEqual(data["selected_answer"], "World")  # Student's answer

    def test_api_returns_correct_answer_for_dropdown(self):
        """Test if the API correctly returns Dropdown correct answer"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, self.dropdown_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["correct_answer"], "CorrectOption")  # Correct answer
        self.assertEqual(data["selected_answer"], "CorrectOption")  # Student's answer

    def test_api_returns_correct_answer_for_match_question(self):
        """Test if API correctly returns match question answer"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, self.match_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["correct_answer"], {"A": "1", "B": "2"})  # Expected output

    def test_api_returns_null_if_no_response(self):
        """Test if API returns null when student hasn't answered"""
        self.client.login(username="teststudent", password="testpass")
        new_question = Question.objects.create(
            poll=self.poll,
            question_type="single_choice",
            question_text="Unanswered Question?"
        )
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, new_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(data["selected_answer"])  # No response yet
        self.assertIn(data["correct_answer"], [[], "No correct answer available"])

    def test_api_returns_404_for_invalid_question(self):
        """Test if API returns 404 when question does not exist"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, 99999]))  # Invalid question
        self.assertEqual(response.status_code, 404)

    def test_api_returns_400_for_invalid_method(self):
        """Test if API returns 400 when method is not GET"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.post(reverse('get_student_answer', args=[self.poll.id, self.mcq_question.id]))
        self.assertEqual(response.status_code, 400)