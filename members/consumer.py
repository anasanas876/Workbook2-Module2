
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
import json


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("CONNECT STARTED")

        try:
            self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
            print("ROOM ID:", self.room_id)

            self.room_group_name = f"chat_{self.room_id}"
            print("GROUP:", self.room_group_name)

            #await self.channel_layer.group_add(
                #self.room_group_name,
                #self.channel_name
            #)

            print("GROUP ADDED")

            await self.accept()

            print("CONNECTION ACCEPTED")

            messages = await self.get_last_messages()
            print("MESSAGES LOADED:", messages)

            for message in reversed(messages):
                await self.send(
                    text_data=message.content
                )

            
            
        # Adding exception to identify a cause of self disconnection
        except Exception as e:
            print("CONNECT ERROR:", repr(e))
            raise

    async def receive(self, text_data):
        # Convert JSON string into Python dictionary
        data = json.loads(text_data)

        # Extract the actual message
        message = data["message"]

        # Save message in database
        await database_sync_to_async(Message.objects.create)(
            sender=self.scope["user"],
            content=message,
            room_id=self.room_id
        )

        # Send message to everyone in this room
        #await self.channel_layer.group_send(
           # self.room_group_name,
           # {
                #"type": "chat_message",
                #"message": message
            #}
            # )

    async def chat_message(self, event):
        await self.send(
            text_data=event["message"]
        )

    async def disconnect(self, close_code):
        print("DISCONNECT METHOD CALLED", close_code)
        print("CLOSE CODE:", close_code)
        print("ROOM:", self.room_id)

        #await self.channel_layer.group_discard(
           # self.room_group_name,
           # self.channel_name
       # )

        
   # Getting Last 20 messages from the specific room
    @database_sync_to_async
    def get_last_messages(self):
        return list(
            Message.objects
            .filter(room=self.room_id)
            .order_by("-timestamp")[:20]
        )

