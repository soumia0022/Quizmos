from django.test import TestCase
from django.contrib.auth import get_user_model
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question  
from response_management.models.response_model import (
    MultipleChoiceResponse,
    SingleChoiceResponse,
    TextFillResponse,
    DropdownFillResponse
)

User = get_user_model()

class ResponseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', role='Student')
        self.poll = Poll.objects.create(
            title="Sample Poll",
            user=self.user,
            number_code=123456
        )

        self.question = Question.objects.create(
            poll=self.poll,  
            question_type="multiple_choice",  
            multiple_choice_question="What is 2 + 2?",  
            multiple_choice_options=["2", "3", "4", "5"]  
        )

    def test_multiple_choice_response_creation(self):
        response = MultipleChoiceResponse.objects.create(
            user=self.user,
            poll=self.poll,
            question=self.question,
            selected_options=["4"]
        )
        
        self.assertEqual(response.user, self.user)
        self.assertEqual(response.poll, self.poll)
        self.assertEqual(response.question, self.question)
        self.assertEqual(response.selected_options, ["4"])
        self.assertIsNotNone(response.submitted_on)
    
    def test_single_choice_response_creation(self):
        response = SingleChoiceResponse.objects.create(
            user=self.user,
            poll=self.poll,
            question=self.question,
            selected_option="4"
        )
        
        self.assertEqual(response.user, self.user)
        self.assertEqual(response.poll, self.poll)
        self.assertEqual(response.question, self.question)
        self.assertEqual(response.selected_option, "4")
        self.assertIsNotNone(response.submitted_on)
    
    def test_text_fill_response_creation(self):
        response = TextFillResponse.objects.create(
            user=self.user,
            poll=self.poll,
            question=self.question,
            answer_text="Four"
        )
        
        self.assertEqual(response.user, self.user)
        self.assertEqual(response.poll, self.poll)
        self.assertEqual(response.question, self.question)
        self.assertEqual(response.answer_text, "Four")
        self.assertIsNotNone(response.submitted_on)
    
    def test_dropdown_fill_response_creation(self):
        response = DropdownFillResponse.objects.create(
            user=self.user,
            poll=self.poll,
            question=self.question,
            selected_option="4"
        )
        
        self.assertEqual(response.user, self.user)
        self.assertEqual(response.poll, self.poll)
        self.assertEqual(response.question, self.question)
        self.assertEqual(response.selected_option, "4")
        self.assertIsNotNone(response.submitted_on)