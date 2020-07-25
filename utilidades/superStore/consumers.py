import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificacionConsumer(WebsocketConsumer):
    def connect(self):
        print("Se ha conectado")
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = 'noti_%s' % str(self.room_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print(self.scope['url_route']['kwargs']['pk'])
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        print(str(text_data))
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("Este es un nuevo mensaje "+str(message))

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'notification_message',
                'messaje':message
            }
        )
        self.send(text_data=json.dumps({
            'message':message
        }))
    def notification_message(self, event):
        message = event['messaje']
        self.send(text_data=json.dumps({
            'message':message
        }))