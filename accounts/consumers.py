from channels.generic.websocket import WebsocketConsumer


class MessageConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data="Hello world!")
        # self.send(bytes_data="Hello world!")

    def disconnect(self, close_code):
        pass
