from asyncio import events
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
from .models import tbl_clients_connect
from .models import tbl_bandeja_de_entrada_cliente, tbl_bandeja_de_salida_cliente, tbl_bandeja_de_entrada_mayorista, tbl_bandeja_de_salida_mayorista
from .models import tbl_producto
from django.core.serializers import serialize
class BuscarProductos(AsyncWebsocketConsumer):
    async def connect(self):
        print('Conectando..')
        await self.accept()
    async def disconnect(self, close_code):
        print('desconectado..')
    async def receive(self, text_data):
        claves=json.loads(text_data)
        clave_nombre=claves['clave_nombre']#para buscar por nombre de producto
        lista_productos= await self.get_producto_nombre(clave_nombre=clave_nombre)#buscando los productos por nombre
        await self.send(text_data=lista_productos)
    
    @database_sync_to_async
    def get_producto_nombre(self, clave_nombre):
        productos=None
        if len(clave_nombre)>0:
            productos = tbl_producto.objects.filter(Q(producto__icontains=clave_nombre.lower())& Q(mayorista__user__id=self.scope['user'].id))
        elif len(clave_nombre)==0:
            productos = tbl_producto.objects.filter(Q(mayorista__user__id=self.scope['user'].id))
        #print(productos)
        list_productos=[]
        productos_json=serialize('json', productos)
        
        return productos_json
        

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
    def guardar_mensaje(self, mensaje):
        tipo_usuario = self.scope['user'].tipo_usuario_id.tipo_usuario
        grupo = self.room_name
        seguidor = tbl_seguidores.objects.get(grupo_privado=grupo)
        cliente=seguidor.cliente
        mayorista=seguidor.mayorista
        if(tipo_usuario=="Cliente"):#si el tipo de usuario es cliente el mensaje se almacena en la bandeja de salida
            men1=tbl_bandeja_de_salida_cliente.objects.create(
                mayorista=mayorista,   
                cliente=cliente,
                mensaje=mensaje,
                fecha=timezone.now(),
                grupo=str(grupo)
            )
            mensaje_salida_anterior = tbl_bandeja_de_salida_mayorista.objects.last()
            print("hOLAAAA")
            print(mensaje_salida_anterior)
            if mensaje_salida_anterior is not None:
                men2=tbl_bandeja_de_entrada_mayorista.objects.create(
                    cliente=cliente,
                    mayorista=mayorista,
                    mensaje_salida=mensaje_salida_anterior,
                    mensaje=mensaje,
                    fecha=timezone.now(),
                    grupo=str(grupo)
                )
            else:
                men2=tbl_bandeja_de_entrada_mayorista.objects.create(
                    cliente=cliente,
                    mayorista=mayorista,
                    mensaje=mensaje,
                    fecha=timezone.now(),
                    grupo=str(grupo)
                )                
            print('men1 '+str(men1.id)+' men2'+str(men2.id))
        else:
            tbl_bandeja_de_salida_mayorista.objects.create(
                cliente=cliente,
                mayorista=mayorista,
                mensaje=mensaje,
                fecha=timezone.now(),
                grupo=str(grupo)
            )    
            mensaje_salida_anterior=tbl_bandeja_de_salida_cliente.objects.last()            
            if mensaje_salida_anterior is not None:
                tbl_bandeja_de_entrada_cliente.objects.create(
                    mayorista=mayorista,
                    cliente=cliente,
                    mensaje_salida=mensaje_salida_anterior,
                    mensaje=mensaje,
                    fecha=timezone.now(),
                    grupo=str(grupo)
                )
            else: 
                tbl_bandeja_de_entrada_cliente.objects.create(
                    mayorista=mayorista,
                    cliente=cliente,
                    mensaje=mensaje,
                    fecha=timezone.now(),
                    grupo=str(grupo)
                )
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
        await self.guardar_mensaje(message)#guardando mensaje   
        
        if tipo_usuario=="Proveedor":
            usuario=await self.get_name_proveedor()

        else:
            usuario = str(self.scope['user'])

        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat_message',
                'message': message,
                'usuario':usuario,
                'tipo_usuario':tipo_usuario,
                'group':group,
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        tipo_usuario = event['tipo_usuario']
        usuario = event['usuario']
        group=event['group']
        await self.send(text_data=json.dumps({
            'message':message,
            'usuario':usuario,
            'tipo_usuario':tipo_usuario,
            'group':group,
        }))

class NotiConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def guardar_canal(self):
        clients = tbl_clients_connect.objects.filter(Q(usuario=self.scope['user']))
        if(clients.exists()!=True):
            tbl_clients_connect.objects.create(
                canal=self.channel_name, 
                usuario=self.scope['user'],
                fecha_connect=timezone.now(),
                estado=True,
            )
        else:
            print(self.channel_name)
            tbl_clients_connect.objects.filter(Q(usuario=self.scope['user'])).update(
                canal=self.channel_name,
                fecha_connect=timezone.now(),
                estado=True
            )
            print("este usuario ya existe: "+str(clients[0].usuario))

    @database_sync_to_async
    def cerrar_canal(self):
        tbl_clients_connect.objects.filter(Q(usuario__id=self.scope['user'].id)).update(
            fecha_disconnect=timezone.now(),
            estado=bool(0)
        )
    
    @database_sync_to_async
    def canal_usuario(self,usuario):
        usuario = User.objects.get(username=usuario)
        canal = tbl_clients_connect.objects.get(usuario=usuario).canal
        return str(canal)


    async def connect(self):
        print("Te has conectado al websocket")
        #print(self.scope)
        await self.guardar_canal()#Guardando o actualizando canal
        self.room_name = self.scope['url_route']['kwargs']['user']
        self.room_group_name = "noti_%s" % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        print("Te has desconectado..")
        await self.cerrar_canal()
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