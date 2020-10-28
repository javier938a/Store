from django.http import request
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.core.serializers import serialize
from superStore.models import tbl_producto, tbl_factura, tbl_venta, tbl_cliente, tbl_factura
from django.db.models import Q
from django.utils import timezone
import json

class OpVender(TemplateView):
    template_name='superStore/proces_vender/op_vender.html'


def listar_productos(request):
    productos=None
    if request.is_ajax():
        productos = tbl_producto.objects.filter(Q(mayorista__user__id=request.user.id))
        print(productos)
    return JsonResponse(serialize('json', productos), safe=False)

def new_factura(request):
    factura=None
    if request.is_ajax():
        factura = tbl_factura.objects.create()

    
    return JsonResponse([{
        'idfactura':str(factura.id),
    }], safe=False)

def efectuar_venta(request):
    resultado=False
    if request.is_ajax():
        if request.method=='POST':
            ventas = json.loads(request.POST.get('venta'))#obteniendo y convirtiendo los datos de las ventas
            for venta in ventas:#recorriendo una por una las venyas
                idcliente=venta['idCliente']
                id_prod=venta['idProducto']
                fecha_hora_realizada=timezone.now()
                producto_name=venta['producto']
                cantidad=int(venta['cantidad'])
                precio=float(venta['precio'].replace('$',''))
                print(type(precio))
                total=float(venta['total'].replace('$',''))
                idfactura=venta['idFactura']
                print(idcliente)
                cliente=tbl_cliente.objects.get(id=idcliente)
                producto=tbl_producto.objects.get(id=id_prod)
                factura=tbl_factura.objects.get(id=idfactura)

                newVenta=tbl_venta(cliente_id=cliente, producto_id=producto, fecha_hora_realizada=fecha_hora_realizada,
                                    cantidad=cantidad, precio_unitario=precio, precio_total=total, factura=factura
                                    )
                newVenta.save()#Guardando la venta
            resultado=True#si es true es porque todas las ventas se han guardado correctamente

                
    
    return JsonResponse({'resultado':resultado}, safe=True)

