from django.test import Client
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from django.urls import re_path
from asgiref.sync import sync_to_async
from poll_management.consumers import PollConsumer
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models import User
import asyncio
from django.test import TransactionTestCase

class TestPollConsumer(TransactionTestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]
    async def asyncSetUp(self):
        # create a test poll
        self.user = await database_sync_to_async(User.objects.get)(username='johndoe')
        self.student = await database_sync_to_async(User.objects.get)(username='janedoe')
        self.poll = await database_sync_to_async(Poll.objects.create)(
            title="Test Poll",
            user=self.user,
            number_code=123456
        )

        self.question = await database_sync_to_async(Question.objects.create)(
            poll=self.poll,
            question_text="Test question?",
            question_type="multiple_choice",
            multiple_choice_options=[],
            multiple_choice_answers=[],
            single_choice_option=[],
            single_choice_answers=[],
            match_options=[],
            match_answers=[]
        )

        self.word_cloud_question = await database_sync_to_async(Question.objects.create)(
            poll=self.poll,
            question_text="Enter your word(s):",
            question_type="wordcloud",
            wordcloud_question="Enter your word(s):"
        )

        self.application = URLRouter([
            re_path(r'ws/poll/(?P<poll_code>\w+)/$', PollConsumer.as_asgi()),
        ])

    def setUp(self):
        self.client = Client()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.asyncSetUp())

    def tearDown(self):
        self.loop.close()
        super().tearDown()

    async def test_connect(self):
        await sync_to_async(self.client.login)(username=self.user.username, password="Password123")
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator.scope['user'] = self.user
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_disconnect(self):
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator.scope['user'] = self.user
        await communicator.connect()
        await communicator.disconnect()

    async def test_receive_question(self):
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator.scope['user'] = self.user
        await communicator.connect()

        message = {'type': 'question', 'question_id': self.question.id}
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'question')
        self.assertEqual(response['question']['id'], self.question.id)
        self.assertEqual(response['question']['text'], "Test question?")
        self.assertEqual(response['question']['type'], "multiple_choice")

        await communicator.disconnect()

    async def test_student_join_count(self):
        """Test that student join counter works correctly"""

        student_communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")


        student_communicator.scope['user'] = self.student  # Student

        # Connect student and check for student count message
        await student_communicator.connect()
        response = await student_communicator.receive_json_from()

        self.assertEqual(response['type'], 'new_student')
        self.assertEqual(response['message'], '1')





    async def test_save_multiple_choice_response(self):
        """Test saving a multiple choice response"""
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator.scope['user'] = self.student
        await communicator.connect()

        # Update test question to have multiple choice options
        await database_sync_to_async(setattr)(
            self.question, 'multiple_choice_options', ['Option A', 'Option B', 'Option C']
        )
        await database_sync_to_async(self.question.save)()

        # Send a response
        message = {
            'type': 'response',
            'question_id': self.question.id,
            'response_type': 'multiple_choice',
            'response_data': ['Option A', 'Option C']
        }
        await communicator.receive_json_from()  # gets the new student message
        await communicator.send_json_to(message)

        # Check response status
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'response_status')
        self.assertTrue(response['success'])

        # Check broadcast message
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'response_update')
        self.assertEqual(response['question_id'], self.question.id)
        self.assertEqual(response['response_type'], 'multiple_choice')
        self.assertEqual(response['user'], self.student.username)

        await communicator.disconnect()

    async def test_save_single_choice_response(self):
        """Test saving a single choice response"""
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator.scope['user'] = self.student
        await communicator.connect()


        # update test question to have single choice options
        await database_sync_to_async(setattr)(
            self.question, 'question_type', 'single_choice'
        )
        await database_sync_to_async(setattr)(
            self.question, 'single_choice_option', ['Yes', 'No', 'Maybe']
        )
        await database_sync_to_async(self.question.save)()

        # send a response
        message = {
            'type': 'response',
            'question_id': self.question.id,
            'response_type': 'single_choice',
            'response_data': 'Yes'
        }
        await communicator.receive_json_from()  # gets the new student message
        await communicator.send_json_to(message)

        # check response status
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'response_status')
        self.assertTrue(response['success'])

        await communicator.disconnect()

    async def test_update_existing_response(self):
        """Test updating an existing response"""
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator.scope['user'] = self.student
        await communicator.connect()

        # First submission
        message = {
            'type': 'response',
            'question_id': self.question.id,
            'response_type': 'text_fill',
            'response_data': 'First answer'
        }
        await communicator.send_json_to(message)
        await communicator.receive_json_from()  # Response status
        await communicator.receive_json_from()  # Broadcast update

        # Second submission (update)
        message['response_data'] = 'Updated answer'
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'response_status')
        self.assertTrue(response['success'])

        await communicator.disconnect()

    async def test_invalid_response_type(self):
        """Test handling of invalid response type"""
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator.scope['user'] = self.student
        await communicator.connect()

        # Send a response with invalid type
        message = {
            'type': 'response',
            'question_id': self.question.id,
            'response_type': 'invalid_type',
            'response_data': 'Some answer'
        }
        await communicator.send_json_to(message)

        # Check response status
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'response_status')
        self.assertFalse(response['success'])

        await communicator.disconnect()

    async def test_match_question_response(self):
        """Test saving a match question response"""
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator.scope['user'] = self.student
        await communicator.connect()

        # Update test question to be a match question
        await database_sync_to_async(setattr)(
            self.question, 'question_type', 'match_question'
        )
        await database_sync_to_async(setattr)(
            self.question, 'match_options', ['A', 'B', 'C']
        )
        await database_sync_to_async(setattr)(
            self.question, 'match_answers', ['1', '2', '3']
        )
        await database_sync_to_async(self.question.save)()

        # Send a response
        match_data = {'A': '1', 'B': '2', 'C': '3'}
        message = {
            'type': 'response',
            'question_id': self.question.id,
            'response_type': 'match_question',
            'response_data': match_data
        }
        await communicator.receive_json_from()  # new student
        await communicator.send_json_to(message)

        # Check response status

        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'response_status')
        self.assertTrue(response['success'])

        await communicator.disconnect()

    async def test_dropdown_response(self):
        """Test saving a dropdown fill response"""
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator.scope['user'] = self.student
        await communicator.connect()

        # Update test question to be a dropdown question
        await database_sync_to_async(setattr)(
            self.question, 'question_type', 'dropdown_fill'
        )
        await database_sync_to_async(setattr)(
            self.question, 'dropdown_options', 'Red,Green,Blue'
        )
        await database_sync_to_async(self.question.save)()

        # Send a response
        message = {
            'type': 'response',
            'question_id': self.question.id,
            'response_type': 'dropdown_fill',
            'response_data': 'Blue'
        }
        await communicator.send_json_to(message)

        # Check response status
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'response_status')
        self.assertTrue(response['success'])

        await communicator.disconnect()

    async def test_invalid_question_id(self):
        """Test handling of invalid question ID"""
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator.scope['user'] = self.student
        await communicator.connect()

        # Send a request with invalid question ID
        message = {
            'type': 'question',
            'question_id': 99999
        }
        await communicator.send_json_to(message)

        # No response expected as the question ID is invalid
        # We're testing that no exception is raised

        await communicator.disconnect()

    async def test_invalid_poll_code(self):
        """Test connecting with invalid poll code"""
        communicator = WebsocketCommunicator(self.application, "/ws/poll/999999/")
        communicator.scope['user'] = self.user
        connected, _ = await communicator.connect()

        # Should not connect with invalid poll code
        self.assertFalse(connected)

    async def test_new_student_message(self):
        """Test manually sending a new_student message"""
        communicator1 = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator2 = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator1.scope['user'] = self.user
        communicator2.scope['user'] = self.user

        await communicator1.connect()
        await communicator2.connect()

        # Send a new_student message directly
        message = {'type': 'new_student', 'message': '5'}
        await communicator1.send_json_to(message)

        # Check that the message is broadcast
        response = await communicator2.receive_json_from()
        self.assertEqual(response['type'], 'new_student')
        self.assertEqual(response['message'], '5')

        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_receive_word_cloud_question(self):
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator.scope['user'] = self.user
        await communicator.connect()

        message = {'type': 'question', 'question_id': self.word_cloud_question.id}
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'question')
        self.assertEqual(response['question']['id'], self.word_cloud_question.id)
        self.assertEqual(response['question']['text'], "Enter your word(s):")
        self.assertEqual(response['question']['type'], "wordcloud")

        await communicator.disconnect()

    async def test_student_join_message(self):
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator.scope['user'] = self.student
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'message')
        self.assertEqual(response['message'], f'A student joined the poll: {self.student.username}!')

        await communicator.disconnect()

    async def test_message_broadcast_to_group(self):
        communicator1 = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator2 = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator1.scope['user'] = self.user
        communicator2.scope['user'] = self.student
        await communicator1.connect()
        await communicator2.connect()

        await communicator1.receive_json_from()
        await communicator2.receive_json_from()

        message = {'type': 'message', 'message': 'Broadcast message'}
        await communicator1.send_json_to(message)

        while True:
            response1 = await communicator1.receive_json_from()
            response2 = await communicator2.receive_json_from()
            if response1['message'] == 'Broadcast message' and response2['message'] == 'Broadcast message':
                break

        self.assertEqual(response1['type'], 'message')
        self.assertEqual(response1['message'], 'Broadcast message')
        self.assertEqual(response2['type'], 'message')
        self.assertEqual(response2['message'], 'Broadcast message')

        await communicator1.disconnect()
        await communicator2.disconnect()
