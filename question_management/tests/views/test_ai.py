from django.test import TestCase
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory
from django.shortcuts import render
from unittest.mock import patch, MagicMock, ANY
import json
import re
import requests
import io
import re
import pytest

from question_management.views.add_question import parse_multiple_choice_questions

from poll_management.models.poll_model import Poll
from question_management.views.add_question import (
    generate_with_ollama,
    parse_multiple_choice_questions,
    generate_simple_questions,
    fallback_questions,
    add_question
)

User = get_user_model()


class UltraComprehensiveCoverageTests(TestCase):
    def setUp(self):

        try:
            from django.contrib.auth.models import Group
            Group.objects.get_or_create(name='Lecturer')
        except Exception:
            pass

        self.user = User.objects.create_user(
            username='testlecturer',
            email='test@example.com',
            password='testpassword'
        )

        try:
            group = Group.objects.get(name='Lecturer')
            self.user.groups.add(group)
        except Exception:
            pass

        self.poll = Poll.objects.create(
            title='Test Poll',
            user=self.user
        )

        self.client = Client()
        self.factory = RequestFactory()
        self.client.force_login(self.user)

    def test_generate_with_ollama_comprehensive(self):

        test_cases = [

            {
                'prompt': "Generate a question about history",
                'mock_response': {
                    'status_code': 200,
                    'text': json.dumps({"response": "Generated text response"})
                },
                'expected_result': "Generated text response"
            },

            {
                'prompt': "x" * 3000,
                'mock_response': {
                    'status_code': 200,
                    'text': json.dumps({"response": "Truncated response"})
                },
                'expected_result': "Truncated response"
            },

            {
                'prompt': "Error test",
                'mock_response': {
                    'status_code': 500,
                    'text': "Internal Server Error"
                },
                'expected_result': ""
            }
        ]

        for case in test_cases:

            with patch('requests.post') as mock_post:

                mock_response = MagicMock()
                mock_response.status_code = case['mock_response']['status_code']
                mock_response.text = case['mock_response']['text']
                mock_post.return_value = mock_response


                result = generate_with_ollama(case['prompt'])


                self.assertEqual(result, case['expected_result'])

    def test_generate_with_ollama_error_handling(self):

        error_cases = [

            {
                'side_effect': requests.exceptions.Timeout(),
                'expected_result': ""
            },

            {
                'side_effect': Exception("Generic error"),
                'expected_result': ""
            }
        ]

        for case in error_cases:

            with patch('requests.post', side_effect=case['side_effect']):

                result = generate_with_ollama("Test prompt")


                self.assertEqual(result, case['expected_result'])

    @patch('question_management.views.add_question.login_required', lambda x: x)
    @patch('user_management.helpers.role_required', lambda x: lambda y: y)
    @patch('django.contrib.auth.decorators.login_required', lambda x: x)
    def test_add_question_additional_scenarios(self):

        additional_test_cases = [

            {
                'method': 'POST',
                'data': {
                    'question_type': 'wordcloud',
                    'youtube_link': 'test_link'
                },
                'mock_handler': 'handle_wordcloud',
                'mock_return': 'sample_wordcloud_image',
                'expected_render': True
            },

            {
                'method': 'POST',
                'data': {
                    'question_type': 'single_choice',
                    'youtube_link': 'test_link'
                },
                'mock_handler': 'handle_single_choice',
                'mock_return': JsonResponse({})
            },

            {
                'method': 'POST',
                'data': {
                    'question_type': 'match_question',
                    'youtube_link': 'test_link'
                },
                'mock_handler': 'handle_match_question',
                'mock_return': JsonResponse({})
            },

            {
                'method': 'POST',
                'data': {
                    'question_type': 'code_question',
                    'youtube_link': 'test_link'
                },
                'mock_handler': 'handle_code_question',
                'mock_return': JsonResponse({})
            }
        ]

        for case in additional_test_cases:

            request = self.factory.post(f'/add_question/{self.poll.id}/', case['data'])
            request.user = self.user
            request.method = 'POST'
            request.POST = case['data']


            mock_manager = MagicMock()
            mock_manager.question_type = case['data'].get('question_type')


            if 'mock_handler' in case:
                handler = getattr(mock_manager, case['mock_handler'])
                handler.return_value = case.get('mock_return')

            try:

                with patch('question_management.views.add_question.QuestionManager',
                           return_value=mock_manager):


                    response = add_question(request, self.poll.id)


                if case.get('expected_render', False):
                    self.assertIsInstance(response, HttpResponse)
                    self.assertEqual(response.template_name[0], "add_question.html")
                    self.assertIn('wordcloud_image', response.context_data)
                else:

                    self.assertIsInstance(response, JsonResponse)


                if 'mock_handler' in case:
                    getattr(mock_manager, case['mock_handler']).assert_called_once()

            except Http404:

                continue
            except Exception as e:
                self.fail(f"Unexpected exception: {e}")

    def test_generate_simple_questions_with_successful_generation(self):

        test_cases = [

            {
                'text': "Short sample text about France",
                'mock_return': """
                Question 1: What is the capital of France?
                A) Paris
                B) London
                C) Berlin
                D) Madrid
                Correct Answer: A
                """,
                'expected_questions': 1
            },

            {
                'text': "x" * 1500,
                'mock_return': """
                Question 1: What is a long text?
                A) Option A
                B) Option B
                C) Option C
                D) Option D
                Correct Answer: B
                """,
                'expected_questions': 1
            }
        ]

        for case in test_cases:

            with patch('question_management.views.add_question.generate_with_ollama',
                       return_value=case['mock_return']):

                result = generate_simple_questions(case['text'])


                self.assertEqual(len(result), case['expected_questions'])
                self.assertEqual(result[0]['question_type'], 'multiple_choice')




from contextlib import contextmanager


@contextmanager
def nullcontext():
    yield None