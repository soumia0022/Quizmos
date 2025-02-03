from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from question_management.models.question_models import Question
#await: is like the waiter saying "I need to wait for the kitchen to finish this order, but I'll serve other tables while waiting"
#async: is like a waiter saying "I'm going to be serving multiple tables"
class PollConsumer(AsyncWebsocketConsumer):
    # This consumer handles WebSocket connections for a polling system
    async def connect(self):
        try:
            #extract the poll_code from the URL route
            self.poll_code = self.scope['url_route']['kwargs']['poll_code']
            # since the poll code is unique, we wil create a group name for this poll
            # so that all clients can receive updates
            self.poll_group_name = f'poll_{self.poll_code}'
        except Exception as e:
            print(f"Error extracting poll code: {e}")

        # Add this connection to the poll group - this allows broadcasting to all connected users
        await self.channel_layer.group_add(
            self.poll_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # When a client disconnects, remove them from the poll group
        await self.channel_layer.group_discard(
            self.poll_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # This handles incoming messages from clients
        # Parse the JSON data received
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        message_content = text_data_json.get('message')
        question_id = text_data_json.get('question_id')

        if message_type == 'message':
            # If it's a regular message, broadcast it to everyone in the poll group
            await self.channel_layer.group_send(
                self.poll_group_name,
                {"type": "poll_message", "message": message_content}
            )
        elif message_type == 'question':
            # If it's a question, fetch it from the database and broadcast it
            question = await self.get_question(question_id)
            if question:
                await self.channel_layer.group_send(
                    self.poll_group_name,
                    {"type": "poll_question", "question": question}
                )

    async def poll_message(self, event):
        # Handler for sending regular messages back to the WebSocket
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message
        }))

    async def poll_question(self, event):
        # Handler for sending questions back to the WebSocket
        question = event['question']

        # Send question to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'question',
            'question': question
        }))

    @database_sync_to_async
    def get_question(self, question_id):
        # Database query to fetch question details
        # Decorated with database_sync_to_async because database operations are synchronous
        try:
            question = Question.objects.get(id=question_id)
            return {
                'id': question.id,
                'text': question.question_text,
                'type': question.question_type,

            }
        except Question.DoesNotExist:
            return None
