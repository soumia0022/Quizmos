from django.test import TestCase
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from django.urls import re_path
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
        self.poll = await database_sync_to_async(Poll.objects.create)(

            title="Test Poll",
            user=self.user,
            number_code = 123456

        )

        #  create the question in the poll
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

        self.application = URLRouter([
            re_path(r'ws/poll/(?P<poll_code>\w+)/$', PollConsumer.as_asgi()),
        ])

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.asyncSetUp())

    def tearDown(self):
        self.loop.close()
        super().tearDown()

    async def test_connect(self):
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_disconnect(self):
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        await communicator.connect()
        await communicator.disconnect()

    async def test_receive_message(self):
        communicator1 = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        communicator2 = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        await communicator1.connect()
        await communicator2.connect()

        message = {'type': 'message', 'message': 'Hello, poll!'}
        await communicator1.send_json_to(message)
        response = await communicator2.receive_json_from()
        self.assertEqual(response['type'], 'message')
        self.assertEqual(response['message'], 'Hello, poll!')

        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_receive_question(self):
        communicator = WebsocketCommunicator(self.application, "/ws/poll/123456/")
        await communicator.connect()

        message = {'type': 'question', 'question_id': self.question.id}
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'question')
        self.assertEqual(response['question']['id'], self.question.id)
        self.assertEqual(response['question']['text'], "Test question?")
        self.assertEqual(response['question']['type'], "multiple_choice")

        await communicator.disconnect()






