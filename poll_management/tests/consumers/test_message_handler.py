from django.test import TransactionTestCase
from channels.db import database_sync_to_async

import json
import asyncio
from poll_management.consumers.poll_consumer_handlers import MessageHandler
from question_management.models.question_models import Question
from poll_management.models.poll_model import Poll
from user_management.models import User


class MockConsumer:
    """Mock consumer for testing MessageHandler"""

    def __init__(self, user, poll, poll_code):
        self.scope = {'user': user}
        self.poll = poll
        self.poll_code = poll_code
        self.poll_group_name = f'poll_{poll_code}'
        self.poll_lock_status = {poll_code: True}  # Default to locked
        self.channel_layer = None  # Will be set during test setup
        self.sent_messages = []

    async def send(self, text_data):
        self.sent_messages.append(json.loads(text_data))

    async def _send_poll_status(self):
        """Mock method to send poll status"""
        await self.send(text_data=json.dumps({
            'type': 'poll_status',
            'status': 'locked' if self.poll_lock_status[self.poll_code] else 'unlocked'
        }))


class TestMessageHandler(TransactionTestCase):
    fixtures = [
        'user_management/tests/fixtures/default_user.json',
        'user_management/tests/fixtures/other_users.json'
    ]

    async def asyncSetUp(self):
        # Set up users
        self.lecturer = await database_sync_to_async(User.objects.get)(username='johndoe')
        await database_sync_to_async(setattr)(self.lecturer, 'role', 'Lecturer')
        await database_sync_to_async(self.lecturer.save)()

        self.student = await database_sync_to_async(User.objects.get)(username='janedoe')
        await database_sync_to_async(setattr)(self.student, 'role', 'Student')
        await database_sync_to_async(self.student.save)()

        # Create poll
        self.poll = await database_sync_to_async(Poll.objects.create)(
            title="Test Poll",
            user=self.lecturer,
            number_code=123456
        )

        # Create question
        self.mcq_question = await database_sync_to_async(Question.objects.create)(
            poll=self.poll,
            question_text="Multiple choice question?",
            question_type="multiple_choice",
            multiple_choice_options=['Option A', 'Option B', 'Option C'],
            multiple_choice_answers=['Option A', 'Option C']
        )

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.asyncSetUp())

    def tearDown(self):
        self.loop.close()
        super().tearDown()

    async def setup_test_channel_layer(self):
        """Set up a test channel layer for the mock consumer"""
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        await channel_layer.flush()
        return channel_layer

    async def test_handle_get_poll_status(self):
        """Test handling get_poll_status message"""
        channel_layer = await self.setup_test_channel_layer()
        mock_consumer = MockConsumer(self.lecturer, self.poll, "123456")
        mock_consumer.channel_layer = channel_layer
        message_handler = MessageHandler(mock_consumer)

        await message_handler.handle_message('get_poll_status', {})

        # Check that poll status was sent
        self.assertEqual(len(mock_consumer.sent_messages), 1)
        self.assertEqual(mock_consumer.sent_messages[0]['type'], 'poll_status')
        self.assertEqual(mock_consumer.sent_messages[0]['status'], 'locked')

    async def test_invalid_message_type(self):
        """Test handling invalid message type"""

        mock_consumer = MockConsumer(self.lecturer, self.poll, "123456")
        message_handler = MessageHandler(mock_consumer)

        await message_handler.handle_message('invalid_type', {})

        self.assertEqual(len(mock_consumer.sent_messages), 0)

    async def test_poll_status_invalid_action(self):
        """Test handling poll_status with invalid action"""
        channel_layer = await self.setup_test_channel_layer()
        mock_consumer = MockConsumer(self.lecturer, self.poll, "123456")
        mock_consumer.channel_layer = channel_layer
        message_handler = MessageHandler(mock_consumer)


        await channel_layer.group_add(mock_consumer.poll_group_name, "test_channel")


        await message_handler.handle_message('poll_status', {'action': 'invalid_action'})

        try:
            await asyncio.wait_for(channel_layer.receive("test_channel"), timeout=0.5)
            self.fail("Invalid action should not trigger a message")
        except asyncio.TimeoutError:
            pass

        await channel_layer.group_discard(mock_consumer.poll_group_name, "test_channel")

    async def test_show_answers_missing_question_id(self):
        """Test show_answers without question_id"""
        # Setup mock consumer with lecturer
        channel_layer = await self.setup_test_channel_layer()
        mock_consumer = MockConsumer(self.lecturer, self.poll, "123456")
        mock_consumer.channel_layer = channel_layer
        message_handler = MessageHandler(mock_consumer)

        # Join the group so we can receive messages
        await channel_layer.group_add(mock_consumer.poll_group_name, "test_channel")

        # Show answers without question_id
        await message_handler.handle_message('show_answers', {
            'action': 'show_answer'
            # No question_id
        })

        try:
            await asyncio.wait_for(channel_layer.receive("test_channel"), timeout=0.5)
            self.fail("Missing question_id should not trigger a message")
        except asyncio.TimeoutError:
            pass  # Expected no message

        await channel_layer.group_discard(mock_consumer.poll_group_name, "test_channel")

    async def test_question_request_missing_question_id(self):
        """Test question request without question_id"""
        # Setup mock consumer
        channel_layer = await self.setup_test_channel_layer()
        mock_consumer = MockConsumer(self.lecturer, self.poll, "123456")
        mock_consumer.channel_layer = channel_layer
        message_handler = MessageHandler(mock_consumer)

        # Join the group so we can receive messages
        await channel_layer.group_add(mock_consumer.poll_group_name, "test_channel")

        # Request question without question_id
        await message_handler.handle_message('question', {
            # No question_id
        })

        # Check that no message was sent
        try:
            await asyncio.wait_for(channel_layer.receive("test_channel"), timeout=0.5)
            self.fail("Missing question_id should not trigger a message")
        except asyncio.TimeoutError:
            pass  # Expected no message

        await channel_layer.group_discard(mock_consumer.poll_group_name, "test_channel")
    async def test_handle_lecturer_status_connected_disconnected(self):
        """Test handling lecturer connection/disconnection status"""
        channel_layer = await self.setup_test_channel_layer()
        mock_consumer = MockConsumer(self.lecturer, self.poll, "123456")
        mock_consumer.channel_layer = channel_layer
        message_handler = MessageHandler(mock_consumer)

        await channel_layer.group_add(mock_consumer.poll_group_name, "test_channel")

        # Send 'connected' action
        await message_handler.handle_message('lecturer_status', {'action': 'connected'})
        self.assertTrue(mock_consumer.lecturer_connected_status["123456"])

        message = await asyncio.wait_for(channel_layer.receive("test_channel"), timeout=0.5)
        self.assertEqual(message['type'], 'lecturer_status_update')
        self.assertEqual(message['action'], 'connected')

        # Send 'disconnected' action
        await message_handler.handle_message('lecturer_status', {'action': 'disconnected'})
        self.assertFalse(mock_consumer.lecturer_connected_status["123456"])

        message = await asyncio.wait_for(channel_layer.receive("test_channel"), timeout=0.5)
        self.assertEqual(message['type'], 'lecturer_status_update')
        self.assertEqual(message['action'], 'disconnected')

        await channel_layer.group_discard(mock_consumer.poll_group_name, "test_channel")


    async def test_check_lecturer_status_connected(self):
        """Student receives 'connected' lecturer status if lecturer is connected."""
        channel_layer = await self.setup_test_channel_layer()

        mock_consumer = MockConsumer(self.student, self.poll, "123456")
        mock_consumer.channel_layer = channel_layer
        mock_consumer.lecturer_connected_status = {"123456": True}  # Lecturer is connected

        handler = MessageHandler(mock_consumer)

        await handler.handle_message("check_lecturer_status", {})

        self.assertEqual(len(mock_consumer.sent_messages), 1)
        self.assertEqual(mock_consumer.sent_messages[0]['type'], 'lecturer_status')
        self.assertEqual(mock_consumer.sent_messages[0]['action'], 'connected')
