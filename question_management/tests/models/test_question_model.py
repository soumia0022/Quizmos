from django.test import TestCase
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question

class QuestionModelTests(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(title="Sample Poll")

    def test_poll_title_property(self):
        question = Question.objects.create(
            poll=self.poll,
            question_text="What is the capital of France?",
            question_type="text_fill"
        )
        self.assertEqual(question.poll_title, "Sample Poll")

    def test_get_dropdown_options_with_options(self):
        question = Question.objects.create(
            poll=self.poll,
            question_text="Select a fruit",
            question_type="dropdown_fill",
            dropdown_options="Apple,Banana,Cherry"
        )
        self.assertEqual(question.get_dropdown_options(), ["Apple", "Banana", "Cherry"])

    def test_get_dropdown_options_without_options(self):
        question = Question.objects.create(
            poll=self.poll,
            question_text="Select a fruit",
            question_type="dropdown_fill",
            dropdown_options=None  # Explicitly setting as None
        )
        self.assertEqual(question.get_dropdown_options(), [])
