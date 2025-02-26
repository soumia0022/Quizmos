from django.test import TestCase, Client
from django.urls import reverse
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User
from question_management.models.question_models import Question
from response_management.models.response_model import (
    MatchQuestionResponse, MultipleChoiceResponse, SingleChoiceResponse, DropdownFillResponse, TextFillResponse
)



class StudentViewResponseTest(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='johndoe')
        self.poll = Poll.objects.create(title='Poll 1', user=self.user, status='active', number_code=111111)

        self.view_url = reverse('poll_management:student_view_poll', kwargs={'poll_id': self.poll.id})

    def test_student_response_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_view_response/poll_response.html')
        self.assertContains(response, self.poll.title)

    def test_student_multiple_choice_response(self):
        multiple_choice_question = Question.objects.create(
            poll=self.poll,
            question_text="Which of the following options do you prefer?",
            question_type='multiple_choice'
        )
        MultipleChoiceResponse.objects.create(
            user=self.user,
            poll=self.poll,
            question=multiple_choice_question,
            selected_options=[1, 2]
        )
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Which of the following options do you prefer?")

    def test_student_single_choice_response(self):
        single_choice_question = Question.objects.create(
            poll=self.poll,
            question_text="What is your favorite color?",
            question_type='single_choice'
        )
        SingleChoiceResponse.objects.create(
            user=self.user,
            poll=self.poll,
            question=single_choice_question,
            selected_option=1
        )
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What is your favorite color?")

    def test_student_text_fill_response(self):
        text_fill_question = Question.objects.create(
            poll=self.poll,
            question_text="Describe your ideal vacation.",
            question_type='text_fill'
        )
        TextFillResponse.objects.create(
            user=self.user,
            poll=self.poll,
            question=text_fill_question,
            answer_text="A beach holiday with lots of sunshine."
        )
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Describe your ideal vacation.")

    def test_student_dropdown_response(self):
        dropdown_question = Question.objects.create(
            poll=self.poll,
            question_text="Select your preferred country.",
            question_type='dropdown'
        )
        DropdownFillResponse.objects.create(
            user=self.user,
            poll=self.poll,
            question=dropdown_question,
            selected_option=1
        )
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select your preferred country.")

    def test_student_match_response(self):
        match_question = Question.objects.create(
            poll=self.poll,
            question_text="Match the following items.",
            question_type='match'
        )
        match_responses = [
            {"item1": "A", "item2": "1"},
            {"item1": "B", "item2": "2"}
        ]
        MatchQuestionResponse.objects.create(
            user=self.user,
            poll=self.poll,
            question=match_question,
            match_responses=match_responses
        )
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Match the following items.")
