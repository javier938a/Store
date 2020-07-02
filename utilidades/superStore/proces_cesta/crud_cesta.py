from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from superStore.models import tbl_cesta, tbl_cliente, tbl_producto, tbl_direccion
from superStore.forms import FormCrearCesta 
from django.urls import reverse_lazy
import datetime
from django.utils import timezone

class ListarCesta(ListView):
    template_name = 'superStore/procesos_cesta/listar_cesta.html'
    context_object_name = 'cesta_list'
    model = tbl_cesta

    def get_queryset(self):
        return self.model.objects.filter(cliente__user__id=self.request.user.id)#pk es el cliente al que esta asociada la cesta

class Agregar_a_Cesta(CreateView):
    model = tbl_cesta
    template_name = 'superStore/procesos_cesta/agregar_a_cesta.html'
    context_object_name = 'form'
    form_class = FormCrearCesta
    def get_context_data(self, **kwargs):
        context = super(Agregar_a_Cesta, self).get_context_data(**kwargs)
        producto = tbl_producto.objects.filter(id=self.kwargs['pk'])
        print("Heloo")
        print(self.request.user.id)
        context.get('form').fields['cliente'].queryset = tbl_cliente.objects.filter(user__id=self.request.user.id)
        context.get('form').fields['producto'].queryset = producto
        precio = producto[0].precio_unitario
        context.get('form').initial = {'precio_unitario':precio,}
        context.get('form').fields['direccion'].queryset = tbl_direccion.objects.filter(cliente__user__id=self.request.user.id)
        return context
    
    def form_valid(self, form):
        precio_unitario = form.cleaned_data['precio_unitario']#Obteniendo el precio unitario
        fecha_transaccion = timezone.now() #Obteniendo la fecha de transaccion
        print(fecha_transaccion)
        cantidad = form.cleaned_data['cantidad']
        print("esta es la cantidad: "+str(cantidad))
        total = float(precio_unitario)*int(cantidad)
        form.instance.precio_total =total
        form.instance.fecha_hora_realizado = fecha_transaccion

        form_valid = super(Agregar_a_Cesta,self).form_valid(form)
        print("Sera que guarda? "+str(total))
        return form_valid
        
    def get_success_url(self):
        return reverse_lazy('tienda:list_cesta')

class ActualizarCesta(UpdateView):
    model = tbl_cesta
    template_name = 'superStore/procesos_cesta/agregar_a_cesta.html'
    context_object_name = 'form'
    form_class = FormCrearCesta

    def form_valid(self, form):
        precio_unitario = form.cleaned_data['precio_unitario']#Obteniendo el precio unitario
        fecha_transaccion = timezone.now() #Obteniendo la fecha de transaccion
        print(fecha_transaccion)
        cantidad = form.cleaned_data['cantidad']
        print("esta es la cantidad: "+str(cantidad))
        total = float(precio_unitario)*int(cantidad)
        form.instance.precio_total =total
        form.instance.fecha_hora_realizado = fecha_transaccion

        form_valid = super(ActualizarCesta,self).form_valid(form)
        print("Sera que guarda? "+str(total))
        return form_valid

    def get_success_url(self):
        return reverse_lazy('tienda:list_cesta', args=[str(self.object.cliente.id)])

class EliminarCesta(DeleteView):
    template_name='superStore/procesos_cesta/eliminar_cesta.html'
    model=tbl_cesta
    form_class=FormCrearCesta
    context_object_name='cesta'
    def get_success_url(self):
        return reverse_lazy('tienda:list_cesta')
