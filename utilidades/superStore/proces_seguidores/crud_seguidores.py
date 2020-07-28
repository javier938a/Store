from django.http import JsonResponse
from django.core.serializers import serialize
from superStore.models import tbl_seguidores, tbl_cliente, tbl_mayorista
from django.db.models import Q
from django.utils import timezone
from fcm_django.models import FCMDevice

def verificar_existe_seguidor(request, pk):
    if request.is_ajax():
        id_user = request.user.id
        seguidor = tbl_seguidores.objects.filter(Q(cliente__user__id=id_user) & Q(mayorista__id=pk)).exists()
        numero_amigos = tbl_seguidores.objects.filter(mayorista__id=pk).count()
        
        print("Numero de amigos "+str(numero_amigos))
        print('Cantidad')
        print(seguidor)
        if seguidor==True:
            return JsonResponse({
                'res':True,
                'numero_amigos':numero_amigos
            }, safe=True)
        print("este el id del proveedor")
        print(pk)
        print("Este es el cliente")
        print(id_user)
    return JsonResponse({
        'res':False,
        'numero_amigos':numero_amigos
    },safe=True)

def agregar_nuevo_seguidor(request, pk):
    #pk el id del proveedor
    seguidor = None
    res=False
    numero_amigos=None
    if request.is_ajax():#Verifica si es una peticion ajax
        id_user = request.user.id#id del usuario
        cliente = tbl_cliente.objects.get(user__id=id_user)#obtiene el cliente logueado
        id_prove = pk
        prove = tbl_mayorista.objects.get(id=id_prove)#obtiene el proveedor al que se quiere seguir
        fecha_de_seguidor = timezone.now()
        print("id prove"+str(prove))
        esta = tbl_seguidores.objects.filter(cliente=cliente, mayorista=prove)
        if esta.exists()==False: #primero se verifica si el cliente existe como seguidor, y si existe se elimina
            seguidor = tbl_seguidores(cliente=cliente, mayorista=prove, fecha_de_seguidor=fecha_de_seguidor)#crea el registro objeto seguidor con el cliente y mayorista 
            seguidor.save()#guarda correctamente
            res=True#si no hay error res cambia a true indicando que se agrego un nuevo amigo
            #obteniendo los seguidores del proveedor
            print('hellowww')
            idProveUser = tbl_mayorista.objects.get(id=id_prove).user.id#Obtiene el id del proveedor al que se le va a enviar la notificacion
            print(idProveUser)
            
            dispositivos = FCMDevice.objects.filter(Q(user_id=idProveUser) & Q(active=True))
            dispositivos.send_message(#Enviando notificacion de que ha agregad nuevo producto
                title= str(request.user) +" te sigue en tu tienda \n un posible cliente!",
                body=str(request.user)+" es tu nuevo seguidor felicidades!!",
                icon='https://i.imgur.com/MZM3K5w.png'
            )
        else:
            seguidor = tbl_seguidores.objects.get(cliente=cliente, mayorista=prove)
            eliminar = seguidor.delete()
            print(" se elimino: "+str(eliminar))
        numero_amigos = tbl_seguidores.objects.filter(mayorista__id=id_prove).count()


            
    return JsonResponse({
        'numero_amigos':numero_amigos,
        'res':res,
    }, safe=True)