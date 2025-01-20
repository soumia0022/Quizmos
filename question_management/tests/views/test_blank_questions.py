from django.test import TestCase, Client
from django.urls import reverse
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll

# Use Selenium and Jest (or Cypress) to test JavaScript code

class AddBlankQuestionViewTests(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(title="Sample Poll")
        self.client = Client()
        self.url = reverse("question_management:add_question", args=[self.poll.id])

    def test_get_add_question_page(self):
        """Test if the add_question page renders successfully."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_question.html")
        self.assertContains(response, self.poll.title)

    def test_add_text_fill_question(self):
        """Test creating a text_fill (text answer) question."""
        data = {
            "question_type": "text_fill",
            "text_fill_question": "What is the capital of England?",
            "text_fill_answer": "London",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Question.objects.filter(
            poll=self.poll,
            question_text="What is the capital of England?",
            question_type="text_fill",
            text_fill_question="What is the capital of England?",
            text_fill_answer="London"
        ).exists())

    def test_add_dropdown_fill_question(self):
        """Test creating a dropdown_fill question."""
        data = {
            "question_type": "dropdown_fill",
            "dropdown_fill_question": "Python is a ____ programming language.",
            "dropdown_correct_answer": "dynamic",
            "additional_options": ["static", "compiled", "functional"],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        question = Question.objects.get(poll=self.poll, question_type="dropdown_fill")
        self.assertEqual(question.dropdown_fill_question, "Python is a ____ programming language.")
        self.assertEqual(question.dropdown_options, "dynamic,static,compiled,functional")


