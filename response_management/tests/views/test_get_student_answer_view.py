from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from response_management.models.response_model import (
    MultipleChoiceResponse, SingleChoiceResponse, DropdownFillResponse, TextFillResponse, WordCloudResponse
)

class GetStudentAnswerViewTest(TestCase):

    def setUp(self):
        """Set up test data before each test"""
        User = get_user_model()
        self.student = User.objects.create_user(username="teststudent", password="testpass")

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

        self.word_cloud_question = Question.objects.create(
            poll=self.poll,
            question_type="word_cloud",
            question_text="Name a famous scientist"
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

        self.word_cloud_response = WordCloudResponse.objects.create(
            user=self.student,
            poll=self.poll,
            question=self.word_cloud_question,
            word_cloud_response=["Einstein", "Tesla"]
        )

    # Regular tests
    def test_api_returns_correct_answer_for_mcq(self):
        """Test if the API correctly returns MCQ correct answer"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, self.mcq_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["correct_answer"], ["4"])
        self.assertEqual(data["selected_answer"], ["4"])

    def test_api_returns_correct_answer_for_single_choice(self):
        """Test if the API correctly returns Single Choice correct answer"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, self.single_choice_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["correct_answer"], ["Paris"])
        self.assertEqual(data["selected_answer"], "Paris")

    def test_api_returns_correct_answer_for_text_fill(self):
        """Test if the API correctly returns Text Fill correct answer"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, self.text_fill_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["correct_answer"], "World")
        self.assertEqual(data["selected_answer"], "World")

    def test_api_returns_correct_answer_for_dropdown(self):
        """Test if the API correctly returns Dropdown correct answer"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, self.dropdown_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["correct_answer"], "CorrectOption")
        self.assertEqual(data["selected_answer"], "CorrectOption")

    # These tests cover the match question handling in the view
    def test_api_returns_mismatch_error_for_match_question(self):
        """Test if API returns mismatch error when match options and answers do not align"""
        self.client.login(username="teststudent", password="testpass")
        mismatched_match_question = Question.objects.create(
            poll=self.poll,
            question_type="match_question",
            question_text="Mismatched Match Question",
            match_options=["A", "B", "C"],  
            match_answers=["1", "2"]  
        )
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, mismatched_match_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["correct_answer"], "Mismatch between options and answers")

    def test_api_returns_correct_format_for_match_question(self):
        """Test if API correctly formats match question answers when options and answers align"""
        self.client.login(username="teststudent", password="testpass")
        well_formed_match_question = Question.objects.create(
            poll=self.poll,
            question_type="match_question",
            question_text="Well-formed Match Question",
            match_options=["X", "Y"],
            match_answers=["Alpha", "Beta"]
        )
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, well_formed_match_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["correct_answer"], [
            {"left": "X", "right": "Alpha"},
            {"left": "Y", "right": "Beta"}
        ])

    def test_error_handling_in_match_questions(self):
        """Test error handling in match questions when an exception occurs"""
        # Create a match question with problematic data that would cause an exception
        problematic_match = Question.objects.create(
            poll=self.poll,
            question_type="match_question",
            question_text="Problematic Match Question",
    )
    
        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, problematic_match.id]))
        data = response.json()
        self.assertEqual(response.status_code, 500)
        self.assertTrue("error" in data)
        self.assertTrue("Error processing match answers" in data["error"])
    
    def test_api_handles_nonexistent_question(self):
        """Test if API correctly handles nonexistent question ID"""
        self.client.login(username="teststudent", password="testpass")
        # Using a non-existent question ID
        nonexistent_id = 9999
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, nonexistent_id]))
        self.assertEqual(response.status_code, 404)

    def test_api_handles_unsupported_question_type(self):
        """Test if API correctly handles unsupported question type"""
        self.client.login(username="teststudent", password="testpass")
        # Create a question with an unsupported type
        unsupported_question = Question.objects.create(
            poll=self.poll,
            question_type="unsupported_type",  # Non-standard type
            question_text="Unsupported Question Type"
        )
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, unsupported_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["correct_answer"], "No correct answer available")

    def test_api_handles_post_method(self):
        """Test if API correctly rejects POST method"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.post(reverse('get_student_answer', args=[self.poll.id, self.mcq_question.id]))
        self.assertEqual(response.status_code, 400)

    def test_api_returns_correct_answer_for_word_cloud(self):
        """Test if the API correctly returns Word Cloud response"""
        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, self.word_cloud_question.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["selected_answer"], ["Einstein", "Tesla"])  # Match what you created in setUp
        self.assertEqual(data["correct_answer"], "No correct answer available") 

    def test_word_cloud_with_no_response(self):
        """Test handling of word cloud questions with no student response"""
        # Create a new word cloud question without any student response
        new_word_cloud = Question.objects.create(
            poll=self.poll,
            question_type="word_cloud",
            question_text="Name a famous painter"
    )

        self.client.login(username="teststudent", password="testpass")
        response = self.client.get(reverse('get_student_answer', args=[self.poll.id, new_word_cloud.id]))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["selected_answer"], None)  
        self.assertEqual(data["correct_answer"], "No correct answer available")
