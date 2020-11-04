from django.http import request, FileResponse
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.core.serializers import serialize
from superStore.models import tbl_producto, tbl_factura, tbl_venta, tbl_cliente, tbl_factura, tbl_mayorista
from django.db.models import Q, Sum
from django.utils import timezone
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter 
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


def ticket(request, pk):
    buffer=None
    if request.method=="GET":
        buffer = io.BytesIO()

        #estandares de ticket 210x98mm(8.26772x3.85827pulgadas)(21x9.8cm)(595.2758x277.7954pt), 210x74mm(8.26772x2.91339pulgadas)(21x7.4cm), 180x60mm(7.08661x2.3622pulgadas)(18x6cm)
        #El encabezado seria de 3cm(1.1811pulgadas)(85.0392pt)
        #cada renglon del encabezado seria de 0.40cm(11.338582677)
        lista_de_ventas=tbl_venta.objects.filter(Q(factura__id=pk))
        
        #calculando la cantidad de espacio de alto que llevara el ticket
        #se sumaria el ancho del encabezado + el ancho del encabezado de la tabla de productos
        espacio_encabezados=85.039370079+19.842519685
        #obteniendo la cantidad de productos que irian en la factura y se multiplicatia por el ancho de cada renglon
        #y se le sumarian 11 lineas mas para tener espacio para el gravado, subtotal, exento, no sujeta, total, efectivo, 'cajero' y fecha y hora de generacion de ticket
        if lista_de_ventas.count()>0:
            cantidad_productos=lista_de_ventas.count()
            espaciosTotalRenglones=cantidad_productos*19.842519685+9.842519685*11
            alto=espacio_encabezados+espaciosTotalRenglones

            #definiendo el tamaño del papel
            ancho=277.7954
            dimensiom=(ancho, alto)
            p=canvas.Canvas(buffer, pagesize=dimensiom)


            #ubicacion del titulo 
            title_y=alto-11.338582677*2
            
            vendedor=tbl_mayorista.objects.get(user__id=request.user.id)
            nombre_empresa =vendedor.nombre_empresa
            
            #Obteniendo la direccion de la empresa
            direccion=str(vendedor.barrio_canton.municipio.departamento)+', '+str(vendedor.barrio_canton.municipio)+', '+str(vendedor.barrio_canton)
            empresa=p.beginText(65, title_y)
            #Cambiandole el tamaño a nombre de empresa
            empresa.setFont('Helvetica', 12)
            empresa.textLine(str(nombre_empresa.upper()))
            p.drawText(empresa)
            
            p.setFont("Helvetica", 5.5)
            #Obteniendo la ubicacion en y de la direccion
            direc_y=alto-11.338582677*3
            p.drawString(8, direc_y, direccion)

            #Obteniendo el objetivo del negocio
            objectivo_negocio=vendedor.objetivo

            #obteniendo la ubicacion en y del objetivo

            object_y=alto-11.338582677*4
            p.drawString(8, object_y, objectivo_negocio)

            factura = tbl_factura.objects.get(id=pk)
            
            #obteniendo el codigo de la factura
            codigo_factura='Ticket: '+factura.numero_factura
            #obteniendo la posicion en y del codigo de factura
            codefact_y=alto-11.338582677*5
            p.drawString(8, codefact_y, codigo_factura)

            enca_y=alto-11.338582677*6
            enca_x1=8
            p.setLineWidth(0.5)
            p.setDash(3,3)
            p.line(enca_x1, enca_y+10, ancho-8, enca_y+10)
            #dibujando una linea inferior del aencabezado
            p.line(enca_x1, enca_y-2.0, ancho-8, enca_y-2.0)
            #primer elemento
            p.drawString(enca_x1,  enca_y, 'CANT.')

            enca_x2=enca_x1+52.35908
            p.drawString(enca_x2, enca_y, 'MEDIDA')

            enca_x3=enca_x2+52.35908
            p.drawString(enca_x3, enca_y, 'ITEM')

            enca_x4 = enca_x3+52.35908
            p.drawString(enca_x4, enca_y, 'PRECIO')

            enca_x5=enca_x4+52.35908
            p.drawString(enca_x5, enca_y, 'TOTAL')

            varia_y=enca_y
            for venta in lista_de_ventas:
                varia_y=varia_y-11.338582677#haciendo variando 
                p.drawString(enca_x1, varia_y, str(venta.cantidad))
                p.drawString(enca_x2, varia_y, "Unidades")
                p.drawString(enca_x3, varia_y, (str(venta.producto_id.producto)))
                text =p.beginText(enca_x4, varia_y)
                text.textLine('')
                text.textLine(('$'+str(venta.precio_unitario)))
                p.drawText(text)
                p.drawString(enca_x5, varia_y, ('$'+str(venta.precio_total)))
            
            #Dibujando la ultima linea punteada        
            p.setLineWidth(0.5)
            p.setDash(3,3)
            pos_pie_line_y=varia_y-11.338582677
            p.line(enca_x1, pos_pie_line_y, ancho-8, pos_pie_line_y)
            #dibujando el total 
            gravado_y=varia_y-11.338582677-5.669291339#retomando el valor con el que quedo varia-y ya que es ahi donde se dibujara el total menos la mitad de un espacio
            gravado_x=enca_x5
            #Obteniendo la suma de todos los precios total
            total = lista_de_ventas.aggregate(Sum('precio_total'))
            print(total)
            p.drawString(gravado_x-52.35908, gravado_y, 'GRAVADO')
            p.drawString(gravado_x, gravado_y, '$'+str(total.get('precio_total__sum')))

            sub_total_y=gravado_y-11.338582677
            sub_total_x=gravado_x
            p.drawString(sub_total_x-52.35908, sub_total_y, 'SUBTOTAL')
            p.drawString(sub_total_x, sub_total_y, '$'+str(total.get('precio_total__sum')))

            exento_x=sub_total_x
            exento_y=sub_total_y-11.338582677
            p.drawString(exento_x, exento_y, '$'+'0.000')
            p.drawString(exento_x-52.35908, exento_y, 'EXENTO')

            nosujeto_x=exento_x
            nosujeto_y=exento_y-11.338582677
            p.drawString(nosujeto_x, nosujeto_y, '$0.000')
            p.drawString(nosujeto_x-52.35908, nosujeto_y, 'NO SUJETA')

            total_x=nosujeto_x
            total_y=nosujeto_y-11.338582677
            p.drawString(total_x, total_y, '$'+str(total.get('precio_total__sum')))
            p.drawString(total_x-52.35908, total_y, 'TOTAL')

        #dibujando las lineas finales

        else:
            p=canvas.Canvas(buffer, pagesize=letter)
            
        p.showPage()
        p.save()

        print(lista_de_ventas)

        buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='ticket.pdf')
        

        


