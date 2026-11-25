import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import traceback

from .models import Notes, Room

def note_to_dict(note):
    return {"id": note.id, "title": note.title, "content": note.content}


class NotesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
     print("CONNECT CALLED", self.scope["path"])
     try:
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.group = f"room_notes_{self.room_id}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        print("GROUP ADDED")
        await self.accept()
        print("ACCEPTED")
     except Exception as e:
        print("CONNECT FAILED:", repr(e))
        raise
    # async def connect(self):
    #     print("CONNECT CALLED", self.scope["path"])
    #     self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
    #     self.group = f"room_notes_{self.room_id}"
    #     await self.channel_layer.group_add(self.group, self.channel_name)
    #     await self.accept()

    async def disconnect(self, code):
        print("Disconnected:", code)
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive(self, text_data):
        print("RECEIVED:", text_data)
        data = json.loads(text_data)
        action = data.get("action")
        content = (data.get("content") or "").strip()
        if not content:
            return

        if action == "create":
            note = await self.create_note(content)
            event = "created"
        elif action == "edit":
            note = await self.edit_note(data.get("id"), content)
            event = "updated"
            if note is None:
                return
        else:
            return

        # broadcast to everyone in the room (including the sender)
        await self.channel_layer.group_send(
            self.group, {"type": "note.event", "event": event, "note": note}
        )

    async def note_event(self, event):
        await self.send(text_data=json.dumps({"event": event["event"], "note": event["note"]}))

    

    @database_sync_to_async
    def create_note(self, content):
     try:
        room = Room.objects.get(id=self.room_id)
        user = self.scope.get("user")
        if not (user and user.is_authenticated):
         user = None

        note = Notes.objects.create(
        title=content[:50],
        content=content,
        room=room,
        workspace=room.workspace,
        user=user,
)
        return note_to_dict(note)
     except Exception:
        traceback.print_exc()
        raise
    @database_sync_to_async
    def edit_note(self, note_id, content):
        try:
            note = Notes.objects.get(id=note_id, room_id=self.room_id)
        except Notes.DoesNotExist:
            return None
        note.content = content
        note.save()
        return note_to_dict(note)