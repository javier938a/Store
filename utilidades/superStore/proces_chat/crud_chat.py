from superStore.models import tbl_bandeja_de_entrada_cliente, tbl_bandeja_de_salida_cliente
from superStore.models import tbl_bandeja_de_entrada_mayorista, tbl_bandeja_de_salida_mayorista
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models import Q

def get_bandeja_de_entrada_cliente(request, grupo):
    bandeja_entrada = None
    bandeja=[]
    if request.method=="GET":
        if request.is_ajax():
            bandeja_entrada = tbl_bandeja_de_entrada_cliente.objects.filter(grupo=grupo)
            for i in bandeja_entrada:
                mensajes={
                    'mayorista':str(i.mayorista),
                    'cliente':str(i.cliente),
                    'mensaje':str(i.mensaje),
                    'fecha':str(i.fecha),
                    'grupo':str(i.grupo)
                }
                bandeja.append(mensajes)
    
    return JsonResponse(
        bandeja,
        safe=True
    )

def get_bandeja_salida_cliente(self, pk):
    bandeja_salida=None
    grupo=None
    salida=None
    if request.method=="GET":
        grupo = request.GET.get('grupo')
        if request.is_ajax():
            bandeja_salida = tbl_bandeja_de_salida_cliente.objects.filter(Q(mensaje_entrada__id=pk)&Q(grupo=grupo))
            for i in bandeja_salida:
                mensaje={
                    'mayorista':str(i.mayorista),
                    'cliente':str(i.cliente),
                    'mensaje':str(i.mensaje),
                    'fecha':str(i.fecha),
                    'grupo':str(i.grupo)
                }
                salida.append(mensaje)
    
    return JsonResponse(
        salida,
        safe=True
    )


def get_bandeja_entrada_mayorista(request, grupo):
    bandeja_entrada = None
    bandeja=[]
    if request.method=="GET":
        if request.is_ajax():
            bandeja_entrada = tbl_bandeja_de_entrada_mayorista.objects.filter(grupo=grupo)
            for i in bandeja_entrada:
                mensaje={
                    'cliente':str(i.cliente),
                    'mayorista':str(i.mayorista),
                    'mensaje':str(i.mensaje),
                    'fecha':str(i.fecha),
                    'grupo':str(i.grupo)
                }
                bandeja.append(mensaje)
    return  bandeja

def get_bandeja_salida_mayorista(request, pk):
    bandeja_salida=None
    bandeja=[]
    grupo=None
    if request.method=='GET':
        if request.is_ajax():
            grupo = request.GET.get('grupo')
            bandeja_salida = tbl_bandeja_de_salida_mayorista.objects.filter(Q(mensaje_entrada__id=pk)&Q(grupo=grupo))
            for i in bandeja_salida:
                mensaje = {
                    'cliente':str(i.cliente),
                    'mayorista':str(i.mayorista),
                    'mensaje':str(i.mensaje),
                    'fecha':str(i.fecha),
                    'grupo':str(i.grupo)
                }
                bandeja.append(mensaje)
    return JsonResponse(
        bandeja,
        safe=True
    )


                

        
