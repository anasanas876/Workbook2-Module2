from django.urls import path
from .consumer import MyConsumer

websocket_urlpatterns = [
    path("ws/test/<str:group_name>/", MyConsumer.as_asgi()),
]