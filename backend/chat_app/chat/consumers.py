import base64
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
import json
from .models import Message, Chat
from django.core.files.base import ContentFile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        self.user = self.scope['user']

        # Accept the connection first
        await self.accept()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Update online participants count
        await self.add_online_participant()

        # Send message to room group that new user joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.update.online',
                'online_participants': await self.get_online_participants(),
            }
        )

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):  # Check if connect was successful
            await self.remove_online_participant()

            # Send message about user leaving
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.update.online',
                    'online_participants': await self.get_online_participants(),
                }
            )

            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat.update.online':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.update.online',
                    'online_participants': await self.get_online_participants()
                }
            )

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
            
        if message_type == 'chat.file':

            chatFile = await self.save_file(data['fileData'])
            if chatFile:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat.file',
                        'file_url': chatFile.file.url,
                        'username': self.scope['user'].username,
                        'timestamp': chatFile.timestamp.strftime("%b %d, %Y %H:%M"),
                        'is_sender': True
                    }
                )

    @database_sync_to_async
    def save_file(self, file_data):
        try:
            format, b64str = file_data.split(';base64,')
            ext = format.split('/')[-1]
            file_bytes = base64.b64decode(b64str)
            chat = Chat.objects.get(id=self.chat_id)
            return Message.objects.create(
                chat=chat,
                sender=self.scope['user'],
                file=ContentFile(file_bytes, name=f"{uuid.uuid4()}.{ext}")
            )
        except Exception as e:
            print(f"Error saving file: {e}")
            return None

    async def chat_file(self, event):
        # Send file message to WebSocket
        event['is_sender'] = self.user.username == event['username']
        await self.send(text_data=json.dumps(event))

    async def chat_message(self, event):
        # Send message to WebSocket
        event['is_sender'] = self.user.username == event['username']
        await self.send(text_data=json.dumps(event))

    async def chat_update_online(self, event):
        # Send online status update to WebSocket
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
    
    @database_sync_to_async
    def add_online_participant(self):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            chat.online_participants = chat.online_participants + 1
            chat.save()
        except Exception as e:
            print(f"Error updating online participants: {e}")

    @database_sync_to_async
    def remove_online_participant(self):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            chat.online_participants = chat.online_participants - 1
            if chat.online_participants < 0:
                chat.online_participants = 0
            chat.save()
        except Exception as e:
            print(f"Error updating online participants: {e}")
    
    @database_sync_to_async
    def get_online_participants(self):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            return chat.online_participants
        except Chat.DoesNotExist:
            return 0
        except Exception as e:
            print(f"Error retrieving online participants: {e}")
            return 0
