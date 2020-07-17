import json
from channels.generic.websocket import WebsocketConsumer

class NotificacionConsumer(WebsocketConsumer):
    def connect(self):
        print("Se ha conectado")
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(str(text_data))
        text_data_json = json.loads(text_data)
        print("Este es el dato ")
        print(type(text_data_json))
        messaje = text_data_json['messaje']
        print("Este es un nuevo mensaje "+str(messaje))
        self.send(text_data=json.dumps({
            'message':messaje
        }))