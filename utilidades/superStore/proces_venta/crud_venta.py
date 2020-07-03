from superStore.models import tbl_venta, tbl_cliente, tbl_producto, tbl_direccion, tbl_estado_envio
from superStore.forms import FormCrearVenta
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, redirect

class RegistrarVenta(CreateView):
    template_name = 'superStore/procesos_venta/registrar_venta.html'
    context_object_name = 'form'
    form_class = FormCrearVenta

    def get_context_data(self, **kwargs):
        context = super(RegistrarVenta, self).get_context_data(**kwargs)
        producto = tbl_producto.objects.filter(id=self.kwargs['pk'])#Obteniendo el producto que el cliente desea comprar
        context.get('form').fields['cliente_id'].queryset = tbl_cliente.objects.filter(user__id=self.request.user.id)#obteniendo el cliente que va comprar el producto
        context.get('form').fields['producto_id'].queryset = producto#obteniendo el producto que va comprar el cliente
        context.get('form').initial={'precio_unitario':producto[0].precio_unitario,}
        context.get('form').fields['direccion'].queryset = tbl_direccion.objects.filter(cliente__user__id=self.request.user.id, estado=True)
        print(context.get('form')['precio_unitario'].value())
        return context
    
    def form_valid(self, form):
        cantidad = form.cleaned_data.get('cantidad')
        precio_unitario = form.cleaned_data.get('precio_unitario')
        total = int(cantidad)*float(precio_unitario)
        #Obteniendo la fecha y hora
        fecha_hora = timezone.now()
        form.instance.precio_total = total
        form.instance.fecha_hora_realizada=fecha_hora
        form.instance.estado_envio=tbl_estado_envio.objects.get(estado='Pendiente')#Poniendo en estado de pendiente cuando se realiza la compra
        form_valid = super(RegistrarVenta, self).form_valid(form)
        return form_valid

    def get_success_url(self):
        return reverse_lazy('tienda:index')
class ListarVenta(ListView):#metodo sirve para listar las ventas del proveedor y las compras en dado caso sea cliente el usuario
    context_object_name = 'venta_list'
    model = tbl_venta
    template_name = 'superStore/procesos_venta/listar_venta.html'

    def get_context_data(self, **kwargs):
        context = super(ListarVenta, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        print("Esto imprime")
        #print(self.kwargs['pk'])
        if str(self.request.user.tipo_usuario_id)=='Cliente':#si es cliente solo listara los productos comprados por esl usuario
            print("Entro al if")
            return tbl_venta.objects.filter(cliente_id__user__id=self.request.user.id)
        return tbl_venta.objects.filter(producto_id__mayorista__user__id=self.request.user.id)#filtrando que solo se muestren las ventas realizada de un determinado proveedor que se especifica con su pk id respectivamente 

class EliminarVenta(DeleteView):
    model = tbl_venta
    template_name = 'superStore/procesos_venta/eliminar_venta.html'
    context_object_name='venta'
    form_class = FormCrearVenta
    def get_context_data(self, **kwargs):
        context = super(EliminarVenta, self).get_context_data(**kwargs)
        print(context)
        return context
    def get_success_url(self):
        return reverse_lazy('tienda:list_venta')

class ModificarEstadoEnvio(TemplateView):
    template_name = 'superStore/procesos_venta/modificar_estado_envio.html'
    def post(self, request, *args, **kwargs):
        cambio = tbl_estado_envio.objects.filter(estado=request.POST['estados'])#Obteniendo el estado del option seleccionadpo
        resultado =tbl_venta.objects.filter(id=self.kwargs['pk']).update(estado_envio=cambio[0].id)#Actualizando el campo utiliano ese estado
        print(resultado)
        return redirect('tienda:list_venta')
  
