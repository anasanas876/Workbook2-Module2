from channels.generic.websocket import WebsocketConsumer


class MyConsumer(WebsocketConsumer):
     # Method accepts a connection requested by client
    def connect(self):
        self.accept()
        