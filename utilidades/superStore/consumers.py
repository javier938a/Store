import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import tbl_mensajes_enviados_cliente, tbl_mensajes_enviados_mayorista, tbl_respuesta_cliente_mayorista, tbl_respuesta_mayorista_cliente, tbl_respuesta_cliente_mayorista
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, AsyncToSync
from channels.db import database_sync_to_async
from .models import tbl_mayorista, tbl_cliente
from django.db.models import Q
from django.utils import timezone
from .models import tbl_seguidores

class ChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def get_tipo_usuario(self):
        return self.scope['user'].tipo_usuario_id.tipo_usuario
    @database_sync_to_async
    def get_name_proveedor(self):
        return tbl_mayorista.objects.get(Q(user__id=self.scope['user'].id)).nombre_empresa
    @database_sync_to_async
    def get_cliente_group(self,grupo):
        seguidor = tbl_seguidores.objects.get(Q(grupo_privado=grupo))
        
        return seguidor.cliente.id

    @database_sync_to_async
    def get_mayorista_group(self, grupo):
        seguidor = tbl_seguidores.objects.get(Q(grupo_privado=grupo))
        return seguidor.mayorista.id

    @database_sync_to_async
    def get_guardar_mensaje_enviado_cliente(self, mensaje, idcliente, idmayorista):
        cliente = tbl_cliente.objects.get(id=idcliente)
        mayorista = tbl_mayorista.objects.get(id=idmayorista)
        mensajes_enviado_del_cliente = tbl_mensajes_enviados_cliente.objects.get_or_create(
            cliente=cliente,
            mayorista=mayorista,
            cuerpo=mensaje,
            fecha_hora=timezone.now()
        )
        if mensajes_enviado_del_cliente[1]==False:
            mensajes_enviado_del_cliente = tbl_mensajes_enviados_cliente.objects.get_or_create(
                cliente=cliente,
                mayorista=mayorista,
                cuerpo=mensaje,
                fecha_hora=timezone.now()
            )
            return mensajes_enviado_del_cliente[0].id
        return mensajes_enviado_del_cliente[0].id
    
    @database_sync_to_async
    def get_guardar_mensaje_enviado_proveedor(self, mensaje, idcliente, idmayorista):
        cliente = tbl_cliente.objects.get(id=idcliente)
        mayorista = tbl_mayorista.objects.get(id=idmayorista)
        mensajes_del_proveedor = tbl_mensajes_enviados_mayorista.objects.get_or_create(
            cliente=cliente,
            mayorista=mayorista,
            cuerpo=mensaje,
            fecha_hora=timezone.now()
        )
        if mensajes_del_proveedor[1]==False:
            mensaje = mensaje+"."
            mensajes_del_proveedor = tbl_mensajes_enviados_mayorista.objects.get_or_create(
                cliente=cliente,
                mayorista=mayorista,
                cuerpo=mensaje,
                fecha_hora=timezone.now()
            )
            return mensajes_del_proveedor[0].id
        return mensajes_del_proveedor[0].id
    
        
    @database_sync_to_async
    def guardar_respuesta_mayorista_cliente(self, idmensaje_cliente, idrespuesta_mayorista):
        mensaje_cliente = tbl_mensajes_enviados_cliente.objects.get(id=idmensaje_cliente)
        respuesta_mayorista = tbl_mensajes_enviados_mayorista.objects.get(id=respuesta_mayorista)
        idsmsRes = tbl_respuesta_mayorista_cliente.objects.get_or_create(
            mensaje_cliente=mensaje_cliente,
            respuesta_mayorista=respuesta_mayorista
        )
    
    def guardar_respuesta_cliente_mayorista(self, respuesta_mayorista, mensaje_cliente):
        respuesta_mayorista = tbl_mensajes_enviados_mayorista.objects.get(id=respuesta_mayorista)
        mensaje_cliente = tbl_mensajes_enviados_cliente.objects.get(id=idmensaje_cliente)
        idsmsres = tbl_respuesta_cliente_mayorista.objects.get_or_create(
            mensaje_mayorista=mensaje_mayorista,
            mensaje_cliente=mensaje_cliente
        )
    async def connect(self):
        print("se ha conectado")
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        tipo_usuario = await self.get_tipo_usuario()
        if(tipo_usuario=="Proveedor"):
            idcliente = await self.get_cliente_group(self.room_name)
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
    
    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Te has desconectado")
    
    async def receive(self, text_data):
        text_data_json=json.loads(text_data)
        message=text_data_json['message']
        tipo_usuario = await self.get_tipo_usuario()
        idCliente = await self.get_cliente_group(self.room_name)
        idmayorista = await self.get_mayorista_group(self.room_name)
        idMensajeProveedor=None#mensaje del provvedor
        idMensajeCliente=None
        
        if(tipo_usuario=="Proveedor"):
            usuario=await self.get_name_proveedor()
            idMensajeMayorista= await self.get_guardar_mensaje_enviado_proveedor(message,idCliente, idmayorista )
            if idMensajeCliente!=None:
                await self.guardar_respuesta_cliente_mayorista(idMensajeMayorista, idMensajeCliente)
        else:
            usuario = str(self.scope['user'])
            idMensajeCliente =await self.get_guardar_mensaje_enviado_cliente(message, idCliente, idmayorista) 
            if idMensajeProveedor !=None:
                await self.guardar_respuesta_mayorista_cliente(idMensajeCliente, idMensajeProveedor)
                
        print("IdMensajeProveedor: "+str(idMensajeProveedor)+" idMensajeCliente: "+str(idMensajeCliente))
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat_message',
                'message': message,
                'usuario':usuario,
                'tipo_usuario':tipo_usuario
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        tipo_usuario = event['tipo_usuario']
        usuario = event['usuario']
        
        await self.send(text_data=json.dumps({
            'message':message,
            'usuario':usuario,
            'tipo_usuario':tipo_usuario,
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