from superStore.models import tbl_producto
from superStore.models import tbl_compras, tbl_mayorista, tbl_cajero
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.core.serializers import serialize
from django.utils import timezone
import json
class Comprar(TemplateView):
    template_name='superStore/proces_compras/comprar_producto.html'


def guardar_compras(request):
    res=False
    if request.is_ajax():
        if request.method=='POST':
            print(request.POST)
            compra = request.POST.get('compras')
            compra_json=json.loads(compra)

            #Obteniendo cada uno de los datos
            for compra in compra_json:
                print(compra)
                idProd=compra['id']#id del producto
                producto=tbl_producto.objects.get(id=idProd)
                nombre_producto=compra['producto']
                cajero=None
                mayorista=None
                if request.user.tipo_usuario_id.tipo_usuario=='cajero':
                    cajero=tbl_cajero.objects.get(user__id=request.user.id)
                else:
                    mayorista=tbl_mayorista.objects.get(user__id=request.user.id) 
                
                fecha_compra=timezone.now()
                cantidad=int(compra['cantidad'])
                precio_compra=float(compra['precio_compra'])
                precio_total=float(compra['precio_total'])

                print("Aqui")
                print(mayorista)
                print(cajero)
                if mayorista!=None:
                    reg_compra=tbl_compras(producto=producto, mayorista=mayorista, fecha_compra=fecha_compra, 
                                        cantidad=cantidad, precio_compra=precio_compra, total_compra=precio_total)
                    reg_compra.save()
                    res=True
                if cajero!=None:
                    reg_compra=tbl_compras(producto=producto, cajero=cajero, fecha_compra=fecha_compra, 
                                        cantidad=cantidad, precio_compra=precio_compra, total_compra=precio_total)
                    reg_compra.save()
                    res=True

    return JsonResponse({'res':res}, safe=True)