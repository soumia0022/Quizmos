from django.test import TestCase
from django.http import HttpRequest
from question_management.views.question_types import get_timer

class TimerTestCase(TestCase):

    def test_valid_timer(self):
        request = HttpRequest()
        request.POST['question_timer'] = '30'
        response = get_timer(request)
        self.assertEqual(response, 30)

    def test_invalid_timer(self):
        request = HttpRequest()
        request.POST['question_timer'] = 'invalid'
        response = get_timer(request)
        self.assertIsNone(response)

    def test_no_timer(self):
        request = HttpRequest()
        response = get_timer(request)
        self.assertIsNone(response)

    def test_empty_timer(self):

        request = HttpRequest()
        request.POST['question_timer'] = ''
        response = get_timer(request)
        self.assertIsNone(response)
