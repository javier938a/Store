import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import tbl_mensajes_enviados_cliente, tbl_mensajes_enviados_mayorista, tbl_respuesta_cliente_mayorista, tbl_respuesta_mayorista_cliente

class NotificacionConsumer(WebsocketConsumer):
    def connect(self):
        print("Se ha conectado")
        print(self.scope['user'])
        print("canal: "+str(self.channel_name))
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        
        print('Nombre del grupo: '+str(self.room_name))
        self.room_group_name = 'noti_%s' % str(self.room_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print(self.scope['url_route']['kwargs']['room_name'])
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        print(str(text_data))
        text_data_json = json.loads(text_data)
        tipo_user = self.scope['user'].tipo_usuario_id.tipo_usuario
        message = str(self.scope['user'])+'--> '+text_data_json['message']
        if tipo_user=='Cliente':
            mensaje_cliente = tbl_mensajes_enviados_cliente()
        else:
            pass

        print("Este es un nuevo mensaje "+str(message))

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'notification_message',
                'messaje':message
            }
        )

    def notification_message(self, event):
        message = event['messaje']
        print('Aqui se envia: '+str(message))
        self.send(text_data=json.dumps({
            'message':message
        }))