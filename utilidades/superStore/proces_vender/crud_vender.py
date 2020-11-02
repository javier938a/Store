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
                stock=venta['stock']#Obteniendo la cantidad de producto que hay en el inventario
                cantidad=int(venta['cantidad'])
                precio=float(venta['precio'].replace('$',''))
                print(type(precio))
                total=float(venta['total'].replace('$',''))
                idfactura=venta['idFactura']
                producto=tbl_producto.objects.get(id=id_prod)
                factura=tbl_factura.objects.get(id=idfactura)

                print(idcliente)
                print("Tamaño del idcliente"+str(idcliente))
                newVenta=None
                if(len(idcliente)>0):#Si se selecciona algun cliente se registra la venta a un cliente 
                    cliente=tbl_cliente.objects.get(id=idcliente)
                    newVenta=tbl_venta(cliente_id=cliente, producto_id=producto, fecha_hora_realizada=fecha_hora_realizada,
                                    cantidad=cantidad, precio_unitario=precio, precio_total=total, factura=factura
                                    )
                else:#de lo contrario se registra la venta sin cliente
                    newVenta=tbl_venta(producto_id=producto, fecha_hora_realizada=fecha_hora_realizada,
                                    cantidad=cantidad, precio_unitario=precio, precio_total=total, factura=factura
                                    )

                newVenta.save()#Guardando la venta
                #calculando el nuevo stock de el inventario y el nuevo precio_unitario(ose precio de compra) y
                #el nuevo precio_venta_total
                prod=tbl_producto.objects.get(Q(id=id_prod))
                precio_compra=float(prod.precio_unitario)#Obteniendo y convirtiendo el precio de compra
                precio_venta_float=float(precio)#convirtiendo el precio de venta traido del backend
                stock_int=int(stock)#convirtiendo en int el stock del producto
                cantidad_int=int(cantidad)#convientiendo en entero la cantidad vendida
                nuevo_stock=stock_int-cantidad_int#obteniendo el nuevo stock del producto

                nuevo_precio_total_venta=nuevo_stock*precio_venta_float#calculando el nuevo precio total de venta 
                nuevo_precio_total_compra=nuevo_stock*precio_compra#calculando el nuevo precio total de compra
            
                # actualizando el stock de cada producto...
                product_update = tbl_producto.objects.filter(Q(id=id_prod)).update(cantidad=nuevo_stock, precio_total=nuevo_precio_total_compra,
                                                             precio_total_venta=nuevo_precio_total_venta)
                print("Actualizando..")
                print('nuevo stock: '+str(nuevo_stock))
                print('nuevo precio total de venta: '+str(nuevo_precio_total_venta))
                print('nuevo precio total de compra: '+str(nuevo_precio_total_compra))
                print(product_update)
            #Actualizando los datos de las facturas
            idFactura = request.POST.get('idfactura')
            codigo_factura= request.POST.get('codigo_factura')
            cliente_factura=request.POST.get('cliente_factura')
            direccion_factura=request.POST.get('direccion_factura')
            nit_factura=request.POST.get('nit_factura')
            #Actualizando los datos de
            factura_update=tbl_factura.objects.filter(id=idFactura).update(numero_factura=codigo_factura, cliente=cliente_factura,
                                                                            Fecha_hora=timezone.now(),direccion=direccion_factura, nit=nit_factura)


            resultado=True#si es true es porque todas las ventas se han guardado correctamente

                
    
    return JsonResponse({'resultado':resultado}, safe=True)

def eliminar_factura(request):
    res=False
    if request.is_ajax():
        if request.method=='POST':
            idFactura=request.POST.get('idfactura')
            print('Factura: '+str(idFactura))
            result = tbl_factura.objects.filter(id=idFactura).delete()
            print("Factura eliminada...")
            print(result)
            res=True
    return JsonResponse({'res':res}, safe=True)

def buscar_producto_barra(request):
    producto_json=None
    if request.is_ajax():
        if request.method=='POST':
            codigo_barra=request.POST.get('codigo_barra')
            producto=tbl_producto.objects.filter(Q(codigo_barra=codigo_barra) & Q(mayorista__user__id=request.user.id))
            producto_json=serialize('json',producto)
            #print(producto_json)
    return JsonResponse(producto_json, safe=False)
        

        


