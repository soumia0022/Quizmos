import json
from channels.generic.websocket import AsyncWebsocketConsumer

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
        message = text_data_json['message']

        # Send message to poll group
        await self.channel_layer.group_send(
            self.poll_group_name,
            {"type": "poll_message", "message": message}
        )

    async def poll_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))