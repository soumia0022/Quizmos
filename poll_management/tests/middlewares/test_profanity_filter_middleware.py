from django.test import TestCase, RequestFactory
from django.http import QueryDict
from unittest.mock import patch, MagicMock
from poll_management.middleware import ProfanityFilterMiddleware, profanity


class ProfanityFilterMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.get_response_mock = MagicMock()
        self.get_response_mock.return_value = "response"
        self.middleware = ProfanityFilterMiddleware(self.get_response_mock)


    @patch('poll_management.middleware.profanity')
    def test_basic_post_request_censoring(self, mock_profanity):
        """Test that POST request data is properly censored."""
        mock_profanity.censor.side_effect = lambda x: x.replace('bad', '***') # make a "bad" word

        post_data = {'field1': 'This is bad text'}
        request = self.factory.post('/test/', post_data)

        response = self.middleware(request)

        # check that bad was censored
        self.assertEqual(request.POST['field1'], 'This is *** text')
        self.get_response_mock.assert_called_once_with(request)

    @patch('poll_management.middleware.profanity')
    def test_post_with_multiple_values_for_field(self, mock_profanity):
        """Test that a field that doesnt have only one value is handled correctly"""
        mock_profanity.censor.side_effect = lambda x: x.replace('bad', '***')

        # create a QueryDict with multiple values for one key
        query_dict = QueryDict('', mutable=True)
        query_dict.appendlist('options', 'bad option 1')
        query_dict.appendlist('options', 'good option')
        query_dict.appendlist('options', 'another bad option')

        request = self.factory.post('/test/')
        request.POST = query_dict

        response = self.middleware(request)

        # check that all values were censored
        self.assertEqual(request.POST.getlist('options'),
                         ['*** option 1', 'good option', 'another *** option'])

    @patch('poll_management.middleware.profanity')
    def test_list_structure_preserved(self, mock_profanity):
        """Test that the structure of list data is preserved."""
        # function to keep track of how many times censor is called
        censored_values = []

        def fake_censor(text):
            censored_values.append(text)
            return text

        mock_profanity.censor.side_effect = fake_censor

        # create a request with multiple fields including list data
        query_dict = QueryDict('', mutable=True)
        query_dict.appendlist('options', 'option 1')
        query_dict.appendlist('options', 'option 2')
        query_dict.appendlist('options', 'option 3')
        query_dict['title'] = 'test title'

        request = self.factory.post('/test/')
        request.POST = query_dict

        response = self.middleware(request)

        # check that lists are preserved
        self.assertEqual(len(request.POST.getlist('options')), 3)
        self.assertEqual(request.POST.getlist('options'), ['option 1', 'option 2', 'option 3'])

        # censor should be called 4 time because there are 4 values
        self.assertEqual(len(censored_values), 4)

    def test_non_string_values_handled(self):
        """Test that non-string values are handled correctly."""
        query_dict = QueryDict('', mutable=True)
        query_dict['string_field'] = 'text value'

        request = self.factory.post('/test/')
        request.POST = query_dict

        with patch.object(QueryDict, 'getlist', return_value=['text value', 123]):
            response = self.middleware(request)

            # there should be no exception
            self.assertEqual(response, "response")

