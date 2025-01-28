from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from question_management.models.question_models import Question

class PollConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.poll_code = self.scope['url_route']['kwargs']['poll_code']
            self.poll_group_name = f'poll_{self.poll_code}'
        except Exception as e:
            print(f"Error extracting poll code: {e}")

        # Join poll group
        await self.channel_layer.group_add(
            self.poll_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave poll group
        await self.channel_layer.group_discard(
            self.poll_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        message_content = text_data_json.get('message')
        question_id = text_data_json.get('question_id')

        if message_type == 'message':
            # Send message to poll group
            await self.channel_layer.group_send(
                self.poll_group_name,
                {"type": "poll_message", "message": message_content}
            )
        elif message_type == 'question':
            # Fetch question from database
            question = await self.get_question(question_id)
            if question:
                await self.channel_layer.group_send(
                    self.poll_group_name,
                    {"type": "poll_question", "question": question}
                )

    async def poll_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message
        }))

    async def poll_question(self, event):
        question = event['question']

        # Send question to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'question',
            'question': question
        }))

    @database_sync_to_async
    def get_question(self, question_id):
        try:
            question = Question.objects.get(id=question_id)
            return {
                'id': question.id,
                'text': question.question_text,
                'type': question.question_type,

            }
        except Question.DoesNotExist:
            return None
