from superStore.models import User, tbl_comentario_producto, tbl_cliente, tbl_producto
from django.views.generic import ListView, CreateView, DeleteView
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.db.models import Q
import os
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
            dic1={'id':i.id,'cliente':i.cliente.user.username,'producto':i.producto.producto, 'comentario':i.comentario, 'puntaje':i.puntaje, 'foto_prueba1':str(i.foto_prueba1),'foto_prueba2':str(i.foto_prueba2),'foto_prueba3':str(i.foto_prueba3),} 
            print(dic1)
            lista_user.append(dic1)     

    return JsonResponse(lista_user, safe=False)
#metodo para subir las imagenes 

def subir_imagen(image_bit, image_name="img_coment.jpg"):
    raiz = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    print("Raiz: "+str(raiz))
    print("Valor de la raiz")
    print(raiz)
    ubi_writer=raiz+"/media/foto_prueba/"+image_name
    with open(ubi_writer, 'wb+') as ubicasion:
        for bin in image_bit.chunks():
            ubicasion.write(bin)

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
        #obteniendo las imagenes.
        foto_prueba1=request.FILES.get('foto_prueba1')
        foto_prueba2 = request.FILES.get('foto_prueba2')
        foto_prueba3=request.FILES.get('foto_prueba3')
        print("y la imagen?")
        print(request.FILES)        
        
        #Creando el comentario
        print("Este es un comentario")
        print(comentario)
        comentar = tbl_comentario_producto(#Creando el objeto comentario
            cliente=cliente,
            producto=producto,
            comentario=comentario,
            puntaje=puntaje,
            foto_prueba1=foto_prueba1,
            foto_prueba2=foto_prueba2,
            foto_prueba3=foto_prueba3
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

def EditarComentar(request):#metodo servira para eliminar un comentario
    res = False
    if request.is_ajax():
        print(request.POST)
        print(request.FILES)
        print("llega hasta aqui? ")
        id_user = request.user.id
        cliente = tbl_cliente.objects.get(user__id=id_user)
        producto_id=request.POST.get('producto_id')
        id_coment=request.POST.get('id_coment')#Obteniendo el id del comentario
        producto = tbl_producto.objects.get(id=producto_id)
        comentario=request.POST.get('comentario')
        puntaje=request.POST.get('puntaje')
        #OBTENIENDO LAS IMAGENES
        foto_prueba1=request.FILES.get('foto_prueba1')
        foto_prueba2 = request.FILES.get('foto_prueba2')
        foto_prueba3=request.FILES.get('foto_prueba3')
        if foto_prueba1 is not None and foto_prueba2 is not None and foto_prueba3 is not None:
            print("LLega hasta aqui?")
            subir_imagen(foto_prueba1, str(foto_prueba1))
            subir_imagen(foto_prueba2, str(foto_prueba2))
            subir_imagen(foto_prueba3, str(foto_prueba3))
        print("helooo")
        print(comentario)
        tbl_comentario_producto.objects.filter(id=id_coment).update(
                                                            cliente=cliente, 
                                                            producto=producto, 
                                                            comentario=comentario, 
                                                            puntaje=puntaje,
                                                            foto_prueba1=("foto_prueba/"+str(foto_prueba1)),
                                                            foto_prueba2=("foto_prueba/"+str(foto_prueba2)),
                                                            foto_prueba3=("foto_prueba/"+str(foto_prueba3))
                                                        )
    res=True
    datos=[{'res':res,},{'res':res,'id':id_coment, 'cliente':str(cliente), 'producto':str(producto), 'comentario':comentario, 'puntaje':puntaje}]
    print("resultado del update")                                            
    print(comentario) 
    return JsonResponse(datos, safe=False)





             

        
    