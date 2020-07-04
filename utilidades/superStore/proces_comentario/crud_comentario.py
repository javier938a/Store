from superStore.models import User, tbl_comentario_producto, tbl_venta, tbl_cliente
from django.views.generic import ListView, CreateView
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import json

def ListarComentario(request):
    res = False
    if request.method=="POST":
        if request.is_ajax():
            producto_id = request.POST.get('producto_id')
            coment = tbl_comentario_producto.objects.filter(producto__id=producto_id) #
            if coment.exists():
                res=True
                return JsonResponse(serialize('json',coment), safe=False)
            
    #print(comentarios)
    return JsonResponse({'res':res}, safe=True)            
    
    

def EscribirComentario(request):
    #obteniendo los datos por el metodo post
    print("Es ajax")
    print(request.is_ajax())
    if request.is_ajax():
        venta_id = request.POST.get('venta_id')
        puntaje = request.POST.get('puntaje')
        coment= request.POST.get('coment')
        #obteniendo la venta 
        venta = tbl_venta.objects.get(id=int(venta_id))

        #Obteniendo el cliente en base al usuario logueado
        user_id = request.user.id
        cliente = tbl_cliente.objects.get(user__id=user_id)
        print(str(cliente))

        #Creando el comentario

        comentar = tbl_comentario_producto(venta=venta, cliente=cliente, puntaje=puntaje, comentario=coment)
        print("Resultado de save")
        comentar.save()



        datos = {
            'cliente':str(cliente),
            'venta':str(venta),
            'puntaje':puntaje,
            'coment':coment
        }
  
    return JsonResponse(datos, safe=True)
        
    