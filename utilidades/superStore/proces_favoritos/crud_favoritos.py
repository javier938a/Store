from superStore.models import tbl_favoritos
from superStore.models import tbl_cliente
from superStore.models import tbl_producto
from django.http import JsonResponse
from django.core.serializers import serialize



def aniadir_favoritos(request, pk):
    respuesta=None
    res=False
    favorito=None
    print("leega aqui?")
    print(request.is_ajax())
    if request.is_ajax():
        print("id prod: "+str(pk))
        cliente_id = request.GET.get('cliente_id')#Obteniendo el idcliente enviado via post
        cliente = tbl_cliente.objects.get(id=cliente_id)
        producto = tbl_producto.objects.get(id=pk)
        if tbl_favoritos.objects.filter(producto__id=pk).exists()==False:#verifica si el usuario ya agrego el producto
            favorito = tbl_favoritos()
            try:
                favorito.producto=producto
                favorito.cliente=cliente
                favorito.save()
                res=True#si se guarda el resultado es verdadero
            except:
                res = False#si hay algun error el resultado es falto            
        else:#añadiendo a favorito el producto
            print(tbl_favoritos.objects.filter(producto__id=pk).delete())
            res=False
            print("Ya existe!")
        
        respuesta = {'res':res}#empaquetantolo en un dicionario
        
    return JsonResponse({'res':res}, safe=True)

        
        
