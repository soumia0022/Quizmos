# poll_consumer_handlers.py
import json
from poll_management.consumers.poll_consumer_db import DatabaseHandler


class MessageHandler:
    """Handles processing of different message types for the PollConsumer."""

    def __init__(self, consumer):
        self.consumer = consumer
        self.db = DatabaseHandler()

    async def handle_message(self, message_type, data):
        """Route message to appropriate handler based on type."""
        handlers = {
            'new_student': self._handle_new_student_message,
            'poll_status': self._handle_poll_status_change,
            'get_poll_status': self._handle_get_poll_status,
            'show_answers': self._handle_show_answers,
            'question': self._handle_question_request,
            'response': self._handle_response_submission,
            'lecturer_status': self._handle_lecturer_status,
            'check_lecturer_status': self._handle_check_lecturer_status
        }

        handler = handlers.get(message_type)
        if handler:
            await handler(data)

    async def _handle_new_student_message(self, data):
        """Process new student message."""
        await self.consumer.channel_layer.group_send(
            self.consumer.poll_group_name,
            {
                "type": "new_student",
                "message": data.get('message')
            }
        )

    async def _handle_poll_status_change(self, data):
        """Handle poll lock/unlock requests."""
        if not self._is_lecturer():
            return

        action = data.get('action')
        if action not in ['lock', 'unlock']:
            return

        # Update lock status
        self.consumer.poll_lock_status[self.consumer.poll_code] = (action == 'lock')

        # Broadcast to all clients
        await self.consumer.channel_layer.group_send(
            self.consumer.poll_group_name,
            {
                'type': 'poll_status_update',
                'action': action
            }
        )

    async def _handle_get_poll_status(self, data):
        """Handle request for current poll status."""
        await self.consumer._send_poll_status()

    async def _handle_lecturer_status(self, data):
        """Handle lecturer connection/disconnection status."""
        if not self._is_lecturer():
            return

        action = data.get('action')
        if action not in ['connected', 'disconnected']:
            return


        if not hasattr(self.consumer, 'lecturer_connected_status'):
            self.consumer.lecturer_connected_status = {}

        self.consumer.lecturer_connected_status[self.consumer.poll_code] = (action == 'connected')

        await self.consumer.channel_layer.group_send(
            self.consumer.poll_group_name,
            {
                'type': 'lecturer_status_update',
                'action': action
            }
        )

    async def _handle_check_lecturer_status(self, data):
        """Handle student request to check if lecturer is connected."""
        if not self._is_student():
            return

        is_connected = False
        if hasattr(self.consumer, 'lecturer_connected_status'):
            is_connected = self.consumer.lecturer_connected_status.get(self.consumer.poll_code, False)

        await self.consumer.send(text_data=json.dumps({
            'type': 'lecturer_status',
            'action': 'connected' if is_connected else 'disconnected'
        }))

    async def _handle_show_answers(self, data):
        """Handle show/hide answers requests."""
        if not self._is_lecturer():
            return

        action = data.get('action')
        question_id = data.get('question_id')

        if not question_id:
            return

        if action == 'show_answer':
            answers = await self.db.get_correct_answers(question_id)
            if answers is not None:
                await self.consumer.channel_layer.group_send(
                    self.consumer.poll_group_name,
                    {
                        'type': 'broadcast_answers',
                        'question_id': question_id,
                        'answers': answers,
                        'action': 'show_answer'
                    }
                )
        elif action == 'hide_answer':
            await self.consumer.channel_layer.group_send(
                self.consumer.poll_group_name,
                {
                    'type': 'broadcast_answers',
                    'question_id': question_id,
                    'answers': None,
                    'action': 'hide_answer'
                }
            )

    async def _handle_question_request(self, data):
        """Handle question broadcast requests."""
        question_id = data.get('question_id')
        if not question_id:
            return

        questions = await self.db.get_all_questions(self.consumer.poll)
        total_questions = len(questions)
        question = await self.db.get_question(question_id)

        # Find question number
        question_number = self._find_question_number(questions, question_id)

        if question:
            await self.consumer.channel_layer.group_send(
                self.consumer.poll_group_name,
                {
                    "type": "poll_question",
                    "question": question,
                    "question_number": question_number,
                    "total_questions": total_questions
                }
            )

    def _find_question_number(self, questions, question_id):
        """Find the position of a question in the list."""
        for i, q in enumerate(questions):
            if int(q.id) == int(question_id):
                return i + 1
        return None

    async def _handle_response_submission(self, data):
        """Handle student response submissions."""
        from poll_management.helpers import apply_profanity_filter

        # Check if poll is locked for students
        if self._is_student() and not self.consumer.poll_lock_status[self.consumer.poll_code]:
            await self.consumer.send(text_data=json.dumps({
                'type': 'response_status',
                'success': False,
                'message': 'Poll is currently locked'
            }))
            return

        # Check if lecturer is connected before accepting responses
        lecturer_connected = False
        if hasattr(self.consumer, 'lecturer_connected_status'):
            lecturer_connected = self.consumer.lecturer_connected_status.get(self.consumer.poll_code, False)

        if self._is_student() and not lecturer_connected:
            await self.consumer.send(text_data=json.dumps({
                'type': 'response_status',
                'success': False,
                'message': 'Lecturer is disconnected, cannot submit responses'
            }))
            return

        # Apply profanity filter
        filtered_data = apply_profanity_filter(data, data.get('type'))

        # Save response
        success = await self.db.save_response(
            self.consumer.scope['user'],
            self.consumer.poll,
            self.consumer.poll.number_code,
            filtered_data.get('question_id'),
            filtered_data.get('response_type'),
            filtered_data.get('response_data')
        )

        # Send response status to sender
        await self.consumer.send(text_data=json.dumps({
            'type': 'response_status',
            'success': success
        }))

        # Broadcast response if successful
        if success:
            await self.consumer.channel_layer.group_send(
                self.consumer.poll_group_name,
                {
                    'type': 'response_update',
                    'question_id': filtered_data.get('question_id'),
                    'response_type': filtered_data.get('response_type'),
                    'user': self.consumer.scope["user"].username
                }
            )

    def _is_student(self):
        """Check if current user is a student."""
        return self.consumer.scope["user"].role == 'Student'

    def _is_lecturer(self):
        """Check if current user is a lecturer."""
        return self.consumer.scope["user"].role == 'Lecturer'