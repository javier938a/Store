from superStore.models import tbl_favoritos
from superStore.models import tbl_cliente
from superStore.models import tbl_producto
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.generic import ListView

class listarFavoritos(ListView):
    #recibira el id de un usuario y listara los productos agregados a favoritos
    template_name = 'superStore/proces_favoritos/listar_favoritos.html'
    context_object_name = 'favoritos'
    model = tbl_favoritos

    def get_context_data(self, **kwargs):
        context = super(listarFavoritos, self).get_context_data(**kwargs)
        id_user = self.request.user.id#Obteniendo el id del usuario
        cliente_id = tbl_cliente.objects.get(user__id=id_user).id#obteniendo el id del cliente en base al id del usuario
        print("helowwww"+str(cliente_id))
        context['cliente_id']=cliente_id#agregando al contexto el id del cliente
        context['id_cli']=self.request.session.get('id_cli')
        return context
    
    def get_queryset(self):
        id_user = self.request.user.id#Obteniendo el id del usuario
        cliente_id = tbl_cliente.objects.get(user__id=id_user).id#obteniendo el id del cliente en base al id del usuario
        return self.model.objects.filter(cliente__id=cliente_id)

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

        
        
