from django.urls import re_path
from .consumer import NotesConsumer

websocket_urlpatterns = [
    re_path(r"ws/rooms/(?P<room_id>\d+)/notes/$", NotesConsumer.as_asgi()),
]