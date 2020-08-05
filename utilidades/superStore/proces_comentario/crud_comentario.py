from superStore.models import User, tbl_comentario_producto, tbl_cliente, tbl_producto
from django.views.generic import ListView, CreateView, DeleteView
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.db.models import Q
import json

def listarComentarios(request, pk):#pk seria el id de un producto especifico
    if request.is_ajax():
        comentarios = tbl_comentario_producto.objects.filter(Q(producto__id=pk))
        lista_user=[]
        existe=False
        existe_coment = tbl_comentario_producto.objects.filter(Q(cliente__user__id=request.user.id)&Q(producto__id=pk))
        if existe_coment.exists():#verificando si existe el comentario
            print(existe_coment)
            existe=True
        
        dicx={'existe':existe}
        lista_user.append(dicx)

        for i in comentarios:
            dic1={'id':i.id,'cliente':i.cliente.user.username,'producto':i.producto.producto, 'comentario':i.comentario, 'puntaje':i.puntaje} 
            lista_user.append(dic1)     

    return JsonResponse(lista_user, safe=False)

def EscribirComentario(request):
    #obteniendo los datos por el metodo post
    print("Es ajax")
    res = False
    print(request.is_ajax())
    if request.is_ajax():
        #Obteniendo el cliente en base al usuario logueado
        user_id = request.user.id
        cliente = tbl_cliente.objects.get(user__id=user_id) 
        #Obteniendo el el id del producto       
        producto_id = request.POST.get('producto_id')
        #Obteniendo el producto con el el id 
        producto = tbl_producto.objects.get(id=producto_id)
        comentario = request.POST.get('coment')
        puntaje = request.POST.get('puntaje')
        #Creando el comentario
        print("Este es un comentario")
        print(comentario)
        comentar = tbl_comentario_producto(#Creando el objeto comentario
            cliente=cliente,
            producto=producto,
            comentario=comentario,
            puntaje=puntaje
        )
        comentar.save()#guandando comentario
        comentarioFin = tbl_comentario_producto.objects.get(Q(cliente__user__id=request.user.id) & Q(producto__id=producto_id))
        id=comentarioFin.id
        cliente=str(comentarioFin.cliente)
        producto=str(comentarioFin.cliente)
        comentario=str(comentarioFin.comentario)
        puntaje=str(comentarioFin.puntaje)

        datos={'id':id, 'cliente':str(cliente), 'producto':str(producto), 'comentario':str(comentario), 'puntaje':str(puntaje), 'res':str(res)}
        print("Resultado de save")
        
        res = True# si se guarda entonces res cambia a True
        coment = json.dumps(datos)
        print(coment)
    return JsonResponse(datos, safe=True)

def EliminarComentario(request, pk):
    res = False
    if request.is_ajax():
        comentario = tbl_comentario_producto.objects.filter(id=pk).delete()#Eliminando el comentario
        res=True#Si todo lo anterior se ejecuta bien entonces se vuelve verdadero
        print("Esto retorno!!")
    
    
    print(pk)
    return JsonResponse(
        {'res':res},
        safe=True
    )

def EditarComentar(request, pk):#metodo servira para eliminar un comentario
    res = False
    if request.is_ajax():
        id_user = request.user.id
        cliente = tbl_cliente.objects.get(user__id=id_user)
        producto_id=request.GET.get('producto_id')
        producto = tbl_producto.objects.get(id=producto_id)
        comentario=request.GET.get('comentario')
        puntaje=request.GET.get('puntaje')
        print("helooo")
        print(comentario)
        tbl_comentario_producto.objects.filter(id=pk).update(
                                                            cliente=cliente, 
                                                            producto=producto, 
                                                            comentario=comentario, 
                                                            puntaje=puntaje
                                                        )
    res=True
    datos=[{'res':res,},{'res':res,'id':pk, 'cliente':str(cliente), 'producto':str(producto), 'comentario':comentario, 'puntaje':puntaje}]
    print("resultado del update")                                            
    print(comentario) 
    return JsonResponse(datos, safe=False)


             

        
    