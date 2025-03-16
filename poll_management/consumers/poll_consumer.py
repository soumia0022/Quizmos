from channels.generic.websocket import AsyncWebsocketConsumer
import json
from poll_management.consumers.poll_consumer_handlers import MessageHandler
from poll_management.consumers.poll_consumer_db import DatabaseHandler


class PollConsumer(AsyncWebsocketConsumer):
    # Class variables for tracking state
    students_joined = {}
    poll_lock_status = {}  # Track lock status for each poll

    async def connect(self):
        """Handle new WebSocket connection."""
        if not await self._setup_connection():
            await self.close()
            return

        # Accept the WebSocket connection
        await self.accept()

        # Initialize handlers
        self.db = DatabaseHandler()
        self.message_handler = MessageHandler(self)

        # Handle student joins and send poll status
        if self._is_student():
            await self._handle_student_join()

        await self._send_poll_status()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        if self._is_student():
            await self._handle_student_leave()

        await self.channel_layer.group_discard(
            self.poll_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Process incoming WebSocket messages."""
        data = json.loads(text_data)
        message_type = data.get('type')

        # Delegate message handling to the message handler
        await self.message_handler.handle_message(message_type, data)

    # Channel layer event handlers
    async def new_student(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_student',
            'message': event['message']
        }))

    async def poll_message(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message']
        }))

    async def poll_status_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'poll_status',
            'action': event['action']
        }))

    async def poll_question(self, event):
        await self.send(text_data=json.dumps({
            'type': 'question',
            'question': event['question'],
            'question_number': event.get('question_number'),
            'total_questions': event.get('total_questions')
        }))

    async def response_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'response_update',
            'question_id': event['question_id'],
            'response_type': event['response_type'],
            'user': event['user']
        }))

    async def broadcast_answers(self, event):
        await self.send(text_data=json.dumps({
            'type': 'answers',
            'question_id': event['question_id'],
            'answers': event['answers'],
            'action': event['action']
        }))

    # Connection setup methods
    async def _setup_connection(self):
        """Setup initial connection parameters and state."""
        try:
            self.poll_code = self.scope['url_route']['kwargs']['poll_code']
            self.poll_group_name = f'poll_{self.poll_code}'
        except Exception as e:
            print(f"Error extracting poll code: {e}")
            return False

        self.poll = await DatabaseHandler.get_poll(self.poll_code)
        if not self.poll:
            return False

        # Initialize state for this poll if needed
        if self.poll_code not in self.students_joined:
            self.students_joined[self.poll_code] = 0

        if self.poll_code not in self.poll_lock_status:
            self.poll_lock_status[self.poll_code] = True

        # Join the channel group
        await self.channel_layer.group_add(
            self.poll_group_name,
            self.channel_name
        )

        return True

    def _is_student(self):
        """Check if current user is a student."""
        return self.scope["user"].role == 'Student'

    async def _handle_student_join(self):
        """Process a student joining the poll."""
        self.students_joined[self.poll_code] += 1
        await self.channel_layer.group_send(
            self.poll_group_name,
            {
                'type': 'new_student',
                'message': f'{self.students_joined[self.poll_code]}'
            })

    async def _handle_student_leave(self):
        """Process a student leaving the poll."""
        self.students_joined[self.poll_code] -= 1
        await self.channel_layer.group_send(
            self.poll_group_name,
            {
                'type': 'new_student',
                'message': f'{self.students_joined[self.poll_code]}'
            })

    async def _send_poll_status(self, data=None):
        """Send current poll lock status."""
        await self.send(text_data=json.dumps({
            'type': 'poll_status',
            'action': 'lock' if self.poll_lock_status[self.poll_code] else 'unlock'
        }))