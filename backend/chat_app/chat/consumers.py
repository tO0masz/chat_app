from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
import json
from .models import Message, Chat

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat.message':
            message = data['message']
            
            # Save message to database
            chat_message = await self.save_message(message)
            
            if chat_message:
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat.message',
                        'message': message,
                        'username': self.scope['user'].username,
                        'timestamp': chat_message.timestamp.strftime("%b %d, %Y %H:%M"),
                        'is_sender': True
                    }
                )

    async def chat_message(self, event):
        # Send message to WebSocket
        event['is_sender'] = self.scope['user'].username == event['username']
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, message):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            return Message.objects.create(
                chat=chat,
                sender=self.scope['user'],
                content=message
            )
        except Exception as e:
            print(f"Error saving message: {e}")
            return None
