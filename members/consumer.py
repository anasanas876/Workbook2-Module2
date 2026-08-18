from channels.generic.websocket import AsyncWebsocketConsumer
import json
from members.models import Message,Room
from channels.db import database_sync_to_async
class MyConsumer(AsyncWebsocketConsumer):

    
    async def connect(self):
        self.group_id = self.scope["url_route"]["kwargs"]["group_name"]

        
        
        await self.channel_layer.group_add(self.group_name,
                                                     self.channel_name)
        @database_sync_to_async
        def check_room(self):
         get_id=Room.objects.get(id=self.group_id)
         check_room=Room.objects.filter(id=get_id)
         
          
         
        @database_sync_to_async
        def get_messages(self):
            return list(
               
            messages= Message.objects.filter(
            room=self.group_id
        ).order_by("-timestamp")[:20]
    )
        
        await self.accept()
        # Getting 20 messages from Database.
        
        

    async def receive(self, text_data):
        data=json.loads(text_data)
        message=data["message"]
        user=data["user"]
        room_name=self.group_id
        Message.objects.create(sender=user,content=message,room=room_name)

    
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