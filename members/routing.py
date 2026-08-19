from django.urls import path
from .consumer import MyConsumer

websocket_urlpatterns = [
    path("ws/test/<str:group_name>/", MyConsumer.as_asgi()),
    path("http://127.0.0.1:8000/rooms/",)
]