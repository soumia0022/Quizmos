from django.test import TestCase
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question
from user_management.models import User
class QuestionModelTests(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]
    def setUp(self):
        self.poll = Poll.objects.create(title="Sample Poll",
                                        user=User.objects.get(username='johndoe'))
        self.poll_timer = Poll.objects.create(title="Sample Poll Timer",user=User.objects.get(username='johndoe'))


    def test_timer_single_choice(self):
        question = Question.objects.create(
            single_choice_question = "What is the Capital of France?",
            single_choice_option = ["Paris", "London", "Berlin", "Madrid"],  # Example options
            single_choice_answers = ["Paris"],
            timer = 30
        )
        self.assertEqual(question.timer, 30)

    def test_timer_multiple_choice(self):
        question = Question.objects.create(
            multiple_choice_question="Which of the following are programming languages?",
            multiple_choice_options=["Python", "Java", "HTML", "CSS"],
            multiple_choice_answers=["Python", "Java"],
            timer=30
        )
        self.assertEqual(question.timer, 30)

    def test_timer_question_text(self):
        question = Question.objects.create(
            text_fill_question ="What is the largest planet in our solar system?",
            text_fill_answer = "Jupiter",
            timer=30
        )
        self.assertEqual(question.timer, 30)

    def test_timer_dropdown_question(self):
        question = Question.objects.create(
            dropdown_fill_question="Select the largest continent.",
            dropdown_options="Asia, Africa, Europe, Antarctica",
            dropdown_correct_answer="Asia",
            timer=30
        )
        self.assertEqual(question.timer, 30)

    def test_timer_wordcloud_question(self):
        question = Question.objects.create(
            wordcloud_question="Describe your dream vacation.",  # Example word cloud question
            timer=30  # Setting the timer to 30 seconds
        )
        self.assertEqual(question.timer, 30)

    def test_match_question(self):
        question = Question.objects.create(
            match_question="Match the capital cities to their countries.",
            match_options=["France", "Germany", "Spain", "Italy"],
            match_answers=["Paris", "Berlin", "Madrid", "Rome"],
            timer=30
        )
        self.assertEqual(question.timer, 30)

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

    def test_get_dropdown_options_with_correct_answer(self):
        question = Question.objects.create(
            poll=self.poll,
            question_text="Select a fruit",
            question_type="dropdown_fill",
            dropdown_options="Apple,Banana,Cherry",
            dropdown_correct_answer="Orange"
        )
        expected_options = ["Apple", "Banana", "Cherry", "Orange"]
        self.assertEqual(question.get_dropdown_options(), expected_options)

    #1. test MCQ , matching , wordcloud +++ (all question types ) with timer and
    # create questions with fields that are needed
    #asert that the timer saved
