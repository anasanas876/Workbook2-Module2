from channels.generic.websocket import WebsocketConsumer


class MyConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def receive(self, text_data):
        self.send(text_data="Server is alive")