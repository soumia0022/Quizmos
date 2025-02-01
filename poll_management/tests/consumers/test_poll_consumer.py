from django.test import TestCase
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from django.urls import re_path
import pytest
from poll_management.consumers import PollConsumer
from question_management.models.question_models import Question


@pytest.mark.asyncio
@pytest.mark.django_db
class TestPollConsumer:
    @pytest.fixture
    async def setup_test_data(self):
        # Create a test question in the database
        self.question = await database_sync_to_async(Question.objects.create)(
            question_text="Test question?",
            question_type="multiple_choice"
        )

        # Create application routing for testing
        self.application = URLRouter([
            re_path(r'ws/poll/(?P<poll_code>\w+)/$', PollConsumer.as_asgi()),
        ])

        yield  # This is where the test runs

        # Cleanup
        await database_sync_to_async(Question.objects.all().delete)()

    async def test_connect(self, setup_test_data):
        communicator = WebsocketCommunicator(self.application, "/ws/poll/test123/")
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()

    async def test_disconnect(self, setup_test_data):
        communicator = WebsocketCommunicator(self.application, "/ws/poll/test123/")
        await communicator.connect()
        await communicator.disconnect()

    async def test_receive_message(self, setup_test_data):
        communicator1 = WebsocketCommunicator(self.application, "/ws/poll/test123/")
        communicator2 = WebsocketCommunicator(self.application, "/ws/poll/test123/")
        await communicator1.connect()
        await communicator2.connect()

        message = {'type': 'message', 'message': 'Hello, poll!'}
        await communicator1.send_json_to(message)
        response = await communicator2.receive_json_from()
        assert response['type'] == 'message'
        assert response['message'] == 'Hello, poll!'

        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_receive_question(self, setup_test_data):
        communicator = WebsocketCommunicator(self.application, "/ws/poll/test123/")
        await communicator.connect()

        message = {'type': 'question', 'question_id': self.question.id}
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response['type'] == 'question'
        assert response['question']['id'] == self.question.id
        assert response['question']['text'] == "Test question?"
        assert response['question']['type'] == "multiple_choice"

        await communicator.disconnect()

    async def test_invalid_question_id(self, setup_test_data):
        communicator = WebsocketCommunicator(self.application, "/ws/poll/test123/")
        await communicator.connect()

        message = {'type': 'question', 'question_id': 99999}
        await communicator.send_json_to(message)
        try:
            await communicator.receive_json_from(timeout=0.1)
            pytest.fail("Should not receive a response for invalid question")
        except TimeoutError:
            pass

        await communicator.disconnect()

    async def test_invalid_message_type(self, setup_test_data):
        communicator = WebsocketCommunicator(self.application, "/ws/poll/test123/")
        await communicator.connect()

        message = {'type': 'invalid_type', 'message': 'This should be ignored'}
        await communicator.send_json_to(message)
        try:
            await communicator.receive_json_from(timeout=0.1)
            pytest.fail("Should not receive a response for invalid message type")
        except TimeoutError:
            pass

        await communicator.disconnect()

    async def test_multiple_clients(self, setup_test_data):
        communicator1 = WebsocketCommunicator(self.application, "/ws/poll/test123/")
        communicator2 = WebsocketCommunicator(self.application, "/ws/poll/test123/")
        await communicator1.connect()
        await communicator2.connect()

        message = {'type': 'message', 'message': 'Hello from client 1'}
        await communicator1.send_json_to(message)
        response = await communicator2.receive_json_from()
        assert response['message'] == 'Hello from client 1'

        message = {'type': 'message', 'message': 'Hello from client 2'}
        await communicator2.send_json_to(message)
        response = await communicator1.receive_json_from()
        assert response['message'] == 'Hello from client 2'

        await communicator1.disconnect()
        await communicator2.disconnect()
