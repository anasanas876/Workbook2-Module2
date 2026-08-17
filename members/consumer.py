from channels.generic.websocket import AsyncWebsocketConsumer
import json
from members.models import Message,Room
from channels.db import database_sync_to_async
class MyConsumer(AsyncWebsocketConsumer):

    
    async def connect(self):
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]

        
        
        await self.channel_layer.group_add(self.group_name,
                                                     self.channel_name)
        @database_sync_to_async
        def check_room(self):
         get_id=Room.objects.get(id=room_id)
         check_room=Room.objects.filter(self.group_name=get_id)
         if check_room is None:


          Room.objects.create(room_name=self.group_name)
          Message.objects.filter(room=self.group_name).order_by("timestamp")[:20]
         else:
           @database_sync_to_async
           def get_messages(self):
            return list(
               
            messages= Message.objects.filter(
            room=self.room
        ).order_by("-timestamp")[:20]
    )
        
        await self.accept()
        # Getting 20 messages from Database.
        previous_messages=Message.objects.filter()
        

    async def receive(self, text_data):
        data=json.loads(text_data)
        message=data["message"]
        user=data["user"]

        Message.objects.create(sender=user,content=message)

    
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type":"chat_message",
                "message":message
            }
        )
    async def chat_message(self,event):
        message=event["message"]

        await self.send(
            text_data=json.dumps({
                "message":message
                })
        
        )