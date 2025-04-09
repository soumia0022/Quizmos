from django.test import TestCase
from unittest.mock import patch
from poll_management.helpers import apply_profanity_filter


class ProfanityFilterTests(TestCase):

    @patch('poll_management.helpers.profanity')
    def test_apply_profanity_filter_match_question(self, mock_profanity):
        mock_profanity.censor.side_effect = lambda text: text.replace('bad', '***')

        test_data = {
            'message_type': 'response',
            'response_type': 'match_question',
            'response_data': [
                {'question': 'What is a bad word?', 'answer': 'A bad word is inappropriate'},
                'This contains a bad word',
                42
            ]
        }

        result = apply_profanity_filter(test_data, 'response')

        filtered_data = result['response_data']

        self.assertEqual(filtered_data[0]['question'], 'What is a *** word?')
        self.assertEqual(filtered_data[0]['answer'], 'A *** word is inappropriate')

        self.assertEqual(filtered_data[1], 'This contains a *** word')

        self.assertEqual(filtered_data[2], 42)

        self.assertEqual(mock_profanity.censor.call_count, 3)

    @patch('poll_management.helpers.profanity')
    def test_apply_profanity_filter_other_response_type(self, mock_profanity):
        mock_profanity.censor.side_effect = lambda text: text.replace('bad', '***')

        test_data = {
            'message_type': 'response',
            'response_type': 'other_type',
            'response_data': [
                'First bad string',
                'Second bad string',
                {'should': 'not filter dict keys for non-match_question'},
                42
            ]
        }

        result = apply_profanity_filter(test_data, 'response')

        filtered_data = result['response_data']

        self.assertEqual(filtered_data[0], 'First *** string')
        self.assertEqual(filtered_data[1], 'Second *** string')

        self.assertEqual(filtered_data[2], {'should': 'not filter dict keys for non-match_question'})

        self.assertEqual(filtered_data[3], 42)

        self.assertEqual(mock_profanity.censor.call_count, 2)