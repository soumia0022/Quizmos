from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
import json
from unittest.mock import patch, MagicMock

from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models import User
from response_management.models.response_model import (
    MatchQuestionResponse, MultipleChoiceResponse,
    SingleChoiceResponse, DropdownFillResponse, TextFillResponse, WordCloudResponse
)
from poll_management.views.get_responses import QuestionResponseCounter, get_question_response_counts


class QuestionResponseCounterTests(TestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]
    def setUp(self):

        self.user = User.objects.get(username='johndoe')
        self.poll = Poll.objects.create(
            title="Test Poll",
            user=self.user,
            number_code=123456)

        self.mcq = Question.objects.create(
            poll=self.poll,
            question_text="Multiple choice question?",
            question_type="multiple_choice",
            multiple_choice_options=["Option A", "Option B", "Option C"],
            multiple_choice_answers=["Option A"]
        )

        self.scq = Question.objects.create(
            poll=self.poll,
            question_text="Single choice question?",
            question_type="single_choice",
            single_choice_option=["Yes", "No", "Maybe"],
            single_choice_answers=["Yes"]
        )

        self.dropdown = Question.objects.create(
            poll=self.poll,
            question_text="Dropdown question?",
            question_type="dropdown_fill",
            dropdown_options="Red,Green,Blue",
        )

        self.text = Question.objects.create(
            poll=self.poll,
            question_text="Text fill question?",
            question_type="text_fill",
        )

        self.match = Question.objects.create(
            poll=self.poll,
            question_text="Match question?",
            question_type="match_question",
            match_options=["A", "B", "C"],
            match_answers=["1", "2", "3"]
        )

        self.word_cloud = Question.objects.create(
            poll=self.poll,
            wordcloud_question="Word cloud question?",
            question_type="wordcloud",

        )

        self.test_users = []
        for i in range(5):
            user = User.objects.create_user(
                username=f'testuser{i}',
                email=f'test{i}@example.com',
                password='password123',
                role= 'Student'
            )
            self.test_users.append(user)

    def test_multiple_choice_responses(self):
        """Test counting multiple choice responses"""
        # responses
        MultipleChoiceResponse.objects.create(
            user=self.test_users[0],
            poll=self.poll,
            question=self.mcq,
            selected_options=["Option A"],
            session_code =123456
        )
        MultipleChoiceResponse.objects.create(
            user=self.test_users[1],
            poll=self.poll,
            question=self.mcq,
            selected_options=["Option A", "Option B"],
            session_code=123456
        )
        MultipleChoiceResponse.objects.create(
            user=self.test_users[2],
            poll=self.poll,
            question=self.mcq,
            selected_options=["Option C"],
            session_code=123456
        )

        # count responses
        counter = QuestionResponseCounter(self.mcq)
        response = counter.get_counts()


        data = json.loads(response.content)
        self.assertEqual(data['question_id'], self.mcq.id)
        self.assertEqual(data['question_type'], 'multiple_choice')

        # expected counts: Option A: 2, Option B: 1, Option C: 1
        self.assertEqual(data['counts']['0'], 2)
        self.assertEqual(data['counts']['1'], 1)
        self.assertEqual(data['counts']['2'], 1)

    def test_single_choice_responses(self):
        """Test counting single choice responses"""
        # responses
        SingleChoiceResponse.objects.create(
            user=self.test_users[0],
            poll=self.poll,
            question=self.scq,
            selected_option="Yes",
            session_code=123456
        )
        SingleChoiceResponse.objects.create(
            user=self.test_users[1],
            poll=self.poll,
            question=self.scq,
            selected_option="No",
            session_code=123456
        )
        SingleChoiceResponse.objects.create(
            user=self.test_users[2],
            poll=self.poll,
            question=self.scq,
            selected_option="Yes",
            session_code=123456
        )

        # count responses
        counter = QuestionResponseCounter(self.scq)
        response = counter.get_counts()


        data = json.loads(response.content)
        self.assertEqual(data['question_id'], self.scq.id)
        self.assertEqual(data['question_type'], 'single_choice')

        # Expected counts: Yes: 2, No: 1, Maybe: 0
        self.assertEqual(data['counts']['0'], 2)
        self.assertEqual(data['counts']['1'], 1)
        self.assertEqual(data['counts']['2'], 0)

    def test_dropdown_responses(self):
        """Test counting dropdown responses"""
        #responses
        DropdownFillResponse.objects.create(
            user=self.test_users[0],
            poll=self.poll,
            question=self.dropdown,
            selected_option="Red",
            session_code=123456
        )
        DropdownFillResponse.objects.create(
            user=self.test_users[1],
            poll=self.poll,
            question=self.dropdown,
            selected_option="Blue",
            session_code=123456
        )
        DropdownFillResponse.objects.create(
            user=self.test_users[2],
            poll=self.poll,
            question=self.dropdown,
            selected_option="Red",
            session_code=123456
        )

        # count responses
        counter = QuestionResponseCounter(self.dropdown)
        response = counter.get_counts()

        data = json.loads(response.content)
        self.assertEqual(data['question_id'], self.dropdown.id)
        self.assertEqual(data['question_type'], 'dropdown_fill')

        # Expected counts: Red: 2, Green: 0, Blue: 1
        self.assertEqual(data['counts']['0'], 2)
        self.assertEqual(data['counts']['1'], 0)
        self.assertEqual(data['counts']['2'], 1)

    def test_text_fill_responses(self):
        """Test collecting text fill responses"""
        # responses
        TextFillResponse.objects.create(
            user=self.test_users[0],
            poll=self.poll,
            question=self.text,
            answer_text="First answer",
            session_code=123456
        )
        TextFillResponse.objects.create(
            user=self.test_users[1],
            poll=self.poll,
            question=self.text,
            answer_text="Second answer",
            session_code=123456
        )
        TextFillResponse.objects.create(
            user=self.test_users[2],
            poll=self.poll,
            question=self.text,
            answer_text="   ",  # empty answer that should be filtered out
            session_code=123456
        )

        # count responses
        counter = QuestionResponseCounter(self.text)
        response = counter.get_counts()

        data = json.loads(response.content)
        self.assertEqual(data['question_id'], self.text.id)
        self.assertEqual(data['question_type'], 'text_fill')

        # Should return list of text responses, excluding empty ones
        self.assertEqual(len(data['responses']), 2)
        self.assertIn("First answer", data['responses'])
        self.assertIn("Second answer", data['responses'])

    def test_match_question_responses(self):
        """Test counting match question responses"""
        # responses
        MatchQuestionResponse.objects.create(
            user=self.test_users[0],
            poll=self.poll,
            question=self.match,
            match_responses=[
                {'left': 'A', 'right': '1'},
                {'left': 'B', 'right': '2'},
                {'left': 'C', 'right': '3'}
            ],
            session_code=123456
        )
        MatchQuestionResponse.objects.create(
            user=self.test_users[1],
            poll=self.poll,
            question=self.match,
            match_responses=[
                {'left': 'A', 'right': '2'},
                {'left': 'B', 'right': '3'},
                {'left': 'C', 'right': '1'}
            ],
            session_code=123456
        )

        # count responses
        counter = QuestionResponseCounter(self.match)
        response = counter.get_counts()

        data = json.loads(response.content)
        self.assertEqual(data['question_id'], self.match.id)
        self.assertEqual(data['question_type'], 'match_question')
        self.assertEqual(data['total_responses'], 2)


        counts = data['counts']
        self.assertEqual(counts['A']['1'], 1)
        self.assertEqual(counts['A']['2'], 1)
        self.assertEqual(counts['A']['3'], 0)
        self.assertEqual(counts['B']['2'], 1)
        self.assertEqual(counts['B']['3'], 1)
        self.assertEqual(counts['C']['1'], 1)
        self.assertEqual(counts['C']['3'], 1)

    def test_word_cloud_responses(self):
        """Test collecting word cloud responses"""
        # responses
        WordCloudResponse.objects.create(
            user=self.test_users[0],
            poll=self.poll,
            question=self.word_cloud,
            word_cloud_response= ["hello", "world"],
            session_code=123456
        )
        WordCloudResponse.objects.create(
            user=self.test_users[1],
            poll=self.poll,
            question=self.word_cloud,
            word_cloud_response =["hello", "hi"],
            session_code=123456
        )
        WordCloudResponse.objects.create(
            user=self.test_users[2],
            poll=self.poll,
            question=self.word_cloud,
            word_cloud_response=[],  # empty answer that should be filtered out
            session_code=123456
        )

        # count responses
        counter = QuestionResponseCounter(self.word_cloud)
        response = counter.get_counts()

        data = json.loads(response.content)
        self.assertEqual(data['question_id'], self.word_cloud.id)
        self.assertEqual(data['question_type'], 'wordcloud')


        self.assertEqual(len(data['word_cloud_data']), 3) # hello: 2, hi :1, world:1
        self.assertEqual(data['word_cloud_data']['hello'], 2)
        self.assertEqual(data['word_cloud_data']['hi'], 1)
        self.assertEqual(data['word_cloud_data']['world'], 1)

    def test_get_question_response_counts_function(self):
        """Test the view function that uses the counter class"""

        #a mock request
        request = MagicMock()

        # valid question
        response = get_question_response_counts(request, self.poll.number_code, self.mcq.id)
        self.assertEqual(response.status_code, 200)

        #invalid question id
        response = get_question_response_counts(request, self.poll.number_code, 999999)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

