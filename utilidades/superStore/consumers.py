import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, AsyncToSync
from channels.db import database_sync_to_async
from .models import tbl_mayorista, tbl_cliente
from django.db.models import Q
from django.utils import timezone
from .models import tbl_seguidores
from .models import tbl_mensaje_cliente, tbl_mensaje_mayorista, tbl_respuesta_cliente, tbl_respuesta_mayorista

class ChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def get_tipo_usuario(self):
        return self.scope['user'].tipo_usuario_id.tipo_usuario
    @database_sync_to_async
    def get_name_proveedor(self):
        return tbl_mayorista.objects.get(Q(user__id=self.scope['user'].id)).nombre_empresa
    @database_sync_to_async
    def get_idUser_group(self,grupo):
        idUsuario=None
        seguidor = tbl_seguidores.objects.get(Q(grupo_privado=grupo))
        if self.scope['user'].tipo_usuario_id.tipo_usuario=='Cliente':
            idUsuario = seguidor.cliente.id
        else:
            idUsuario = seguidor.mayorista.id
        return idUsuario

    @database_sync_to_async
    def guardar_mensaje_prove_client(self, tipo_usuario, mensaje, grupo_privado):
        id_mensaje_client_usuario =None

        if tipo_usuario=="Cliente":
            cliente = tbl_seguidores.objects.get(grupo_privado=grupo_privado).cliente#obteniendo el cliente en base añ grupo
    
            id_mensaje_client_usuario=tbl_mensaje_cliente.objects.get_or_create(
                cliente=cliente,
                mensaje=mensaje,
                fecha_envio=timezone.now(),
                grupo_privado=grupo_privado
            )
        else:
            mayorista = tbl_seguidores.objects.get(grupo_privado=grupo_privado).mayorista
            
            id_mensaje_client_usuario = tbl_mensaje_mayorista.objects.get_or_create(
               mayorista=mayorista,
               mensaje=mensaje,
               fecha_envio=timezone.now(),
               grupo_privado=grupo_privado 
            )
        return id_mensaje_client_usuario[0].id
    
    @database_sync_to_async
    def respuesta_mensaje_client_prove(self,tipo_usuario, id_mensaje_cliente, id_mensaje_mayorista):
        id_respuesta_client_prove=None
        mensaje_cliente = tbl_mensaje_cliente.objects.get(id=id_mensaje_cliente)
        mensaje_mayorista = tbl_mensaje_mayorista.objects.get(id=id_mensaje_mayorista)

        if tipo_usuario=="Cliente":
            id_respuesta_client_prove = tbl_respuesta_cliente.objects.get_or_create(
                mensaje_cliente=mensaje_cliente,
                mensaje_mayorista=mensaje_mayorista
            )
        else:
            id_respuesta_client_prove = tbl_respuesta_mayorista.objects.get_or_create(
                mensaje_mayorista=mensaje_mayorista,
                mensaje_cliente=mensaje_cliente
            )
        return id_respuesta_client_prove[0].id
            

    async def connect(self):
        print("se ha conectado")
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        tipo_usuario = await self.get_tipo_usuario()
        if(tipo_usuario=="Proveedor"):
            idcliente = await self.get_idUser_group(self.room_name)
            print("id del cliente: "+str(idcliente))
            proveedor = await self.get_name_proveedor()
            print("Proveedor: "+str(proveedor))
        print("se ha conectado el usuario: "+str(self.scope['user'])+"tipo de usuario: "+str(tipo_usuario))
        
        self.room_group_name="chat_%s" % self.room_name

        print("unido al grupo: "+str(self.room_name))
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Te has desconectado")
    
    async def receive(self, text_data):
        text_data_json=json.loads(text_data)
        message=text_data_json['message']
        group = text_data_json['group']
        tipo_usuario = await self.get_tipo_usuario()
        grupo_privado = self.room_name
        id_mensaje_cliente=0
        id_mensaje_prove=0
        if 'id_mensaje_cliente' in text_data_json:
            id_mensaje_cliente=text_data_json['id_mensaje_cliente']
        
        if 'id_mensaje_prove' in text_data_json:
            id_mensaje_prove = text_data_json['id_mensaje_prove']
        
        if tipo_usuario=="Proveedor":
            usuario=await self.get_name_proveedor()
            id_mensaje_prove = await self.guardar_mensaje_prove_client(tipo_usuario, message, grupo_privado)
            if id_mensaje_cliente > 0:
                id_respuesta_cliente = await self.respuesta_mensaje_client_prove(tipo_usuario ,id_mensaje_cliente, id_mensaje_prove)
                print(str(id_mensaje_cliente)+" es respuesta de "+str(id_mensaje_prove)+" igual a "+str(id_respuesta_cliente))
        else:
            usuario = str(self.scope['user'])
            id_mensaje_cliente = await self.guardar_mensaje_prove_client(tipo_usuario, message, grupo_privado)
            if id_mensaje_prove > 0:
                id_respuesta_prove = await self.respuesta_mensaje_client_prove(tipo_usuario, id_mensaje_cliente, id_mensaje_prove)
                print(str(id_mensaje_prove)+" es respuesta de "+str(id_mensaje_cliente)+" igual a "+str(id_respuesta_prove))

        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat_message',
                'message': message,
                'usuario':usuario,
                'tipo_usuario':tipo_usuario,
                'id_mensaje_cliente':id_mensaje_cliente,
                'id_mensaje_prove':id_mensaje_prove,
                'group':group,
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        tipo_usuario = event['tipo_usuario']
        usuario = event['usuario']
        id_mensaje_cliente = event['id_mensaje_cliente']
        id_mensaje_prove = event['id_mensaje_prove']
        group=event['group']
        await self.send(text_data=json.dumps({
            'message':message,
            'usuario':usuario,
            'tipo_usuario':tipo_usuario,
            'id_mensaje_cliente':id_mensaje_cliente,
            'id_mensaje_prove':id_mensaje_prove,
            'group':group,
        }))

class NotiConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Te has conectado al websocket")
        #print(self.scope)
        self.room_name = self.scope['url_route']['kwargs']['user']
        self.room_group_name = "noti_%s" % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        print("Te has desconectado..")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self,text_data):
        noti = json.loads(text_data)
        grupo=None
        usuario=None
        empresa=None
        if 'grupo' in noti:
            grupo = noti['grupo']
        if 'usuario'in noti:
            usuario = noti['usuario']
        if 'empresa' in noti:
            empresa = noti['empresa']
        
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'noti_message',
                'grupo':grupo,
                'usuario':usuario,
                'empresa':empresa,
            }
        )
        print('grupo: '+str(grupo))
    
    async def noti_message(self, event):
        grupo = event['grupo']
        usuario = event['usuario']
        empresa = event['empresa']
        await self.send(text_data=json.dumps({
            'grupo':grupo,
            'usuario':usuario,
            'empresa':empresa,
        }))



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