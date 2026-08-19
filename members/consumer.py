from channels.generic.websocket import AsyncWebsocketConsumer
import json

from members.models import Message, Room
from channels.db import database_sync_to_async


class MyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_id = self.scope["url_route"]["kwargs"]["group_name"]
        # Calling check_room function to fetch the user requested rom from database
        self.room = await self.check_room()

        await self.channel_layer.group_add(
            self.group_id,
            self.channel_name
        )

        
        await self.accept()

        # Get the last 20 messages from  this room.
        previous_messages = await self.get_messages()

        
        await self.send(
            text_data=json.dumps({
                "type": "previous_messages",
                "messages": previous_messages
            })
        )

    
    @database_sync_to_async
    def check_room(self):
        return Room.objects.get(id=self.group_id)
     # get_messages function gets latest 20 messages from the user joined room
    @database_sync_to_async
    def get_messages(self):

        
        messages = Message.objects.filter(
            room=self.room
        ).order_by("-timestamp")[:20]

        # Using list comprehension to iterate over the messages list
        return [
            {
                "message": message.content,
                "sender": message.sender.username,
                "timestamp": str(message.timestamp)
            }
            for message in messages
        ]
     # Saving new messages in datbase.
    @database_sync_to_async
    def save_message(self, user, message):

        
        Message.objects.create(
            sender=user,
            content=message,
            room=self.room
        )

    

    async def receive(self, text_data):

        # Converting JSON into Python's Dictionary
        data = json.loads(text_data)

        message = data["message"]
        user = self.scope["user"]
        await self.save_message(user, message)

        # Broadcast new message to everyone currently in this room.
        await self.channel_layer.group_send(
            self.group_id,
            {
                "type": "chat_message",
                "message": message
            }
        )

    

    async def chat_message(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps({
                "message": message
            })
        )