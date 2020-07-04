from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from superStore.forms import FormCrearProducto
from superStore.models import tbl_producto, tbl_mayorista

class RegistrarProducto(CreateView):#esta vista sirve para registrar producto se pasa el ID del Mayorista para filtrar que sea el mayorista ingresado
    template_name = 'superStore/procesos_producto/registrar_productos.html'
    form_class = FormCrearProducto
    context_object_name = 'form'
    def get_context_data(self,**kwargs):
        context = super(RegistrarProducto, self).get_context_data(**kwargs)
        context.get('form').fields['mayorista'].queryset = tbl_mayorista.objects.filter(id=self.kwargs['pk'])#Validando que solo el mayorista que ha ingresado seccion vea sus productos en inventario
        return context
    def form_valid(self, form):
        precio_unitario = form.cleaned_data.get('precio_unitario')#Obteniendo el precio unitario del formulario
        cantidad = form.cleaned_data.get('cantidad')#Obteniendo la cantidad total de producto
        total = int(precio_unitario)*float(cantidad)#Obteniendo el precio total del producto
        form.instance.precio_total = total#Agregandolo a el campo del formulario
        form_valid = super(RegistrarProducto, self).form_valid(form)

        return form_valid
    def get_success_url(self):#Definiendo la direccion a donde se tiene que regresar cuando se guarde un producto que es al listado de producto
        return reverse_lazy('tienda:listar_prod', args=[str(self.kwargs['pk'])])

class ListarProductos(ListView):
    template_name = 'superStore/procesos_producto/listar_productos.html'
    model = tbl_producto
    context_object_name = 'prod_list'
    def get_context_data(self, **kwargs):
        context = super(ListarProductos, self).get_context_data(**kwargs)
        context['id_prove']=self.kwargs['pk']
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(mayorista=self.kwargs['pk'])#filtrando que solo sean los productos del mayorista que acaba de iniciar secion sean los que se vean

class EditarProducto(UpdateView):
    template_name = 'superStore/procesos_producto/registrar_productos.html'
    form_class = FormCrearProducto
    model = tbl_producto
    context_object_name = 'form'
    
    def get_context_data(self, **kwargs):
        context = super(EditarProducto, self).get_context_data(**kwargs)
        context.get('form').fields['mayorista'].queryset = tbl_mayorista.objects.filter(user__id=self.request.user.id)
        #context['editar']=1 #servira para validar si se esta usando para registrar o editar
        return context
    
    def get_success_url(self):
        return reverse_lazy('tienda:listar_prod', args=[str(self.kwargs['pk'])] )

class EliminarProducto(DeleteView):
    template_name='superStore/procesos_producto/eliminar_producto.html'
    model = tbl_producto
    form_class = FormCrearProducto
    context_object_name = 'delete_prod'
    def get_context_data(self, **kwargs):
        context = super(EliminarProducto, self).get_context_data(**kwargs)
        context['producto'] = self.get_object()#agrego el objetto
        print("Esto es")
        print(self.get_object().mayorista.id)
        return context
    #el metodo get_object() obtiene el objeto del get_queryset() el objeto espeficio seleccionado
    def get_success_url(self):
        return reverse_lazy('tienda:listar_prod', args=[str(self.get_object().mayorista.id)])
    
class DetalleProducto(DetailView):
    #Recibe como parametro por la url el pk id de un producto especifico
    template_name='superStore/procesos_producto/detalle_producto.html'
    model = tbl_producto
    context_object_name = 'detalle_producto'
    def get_context_data(self, **kwargs):
        context = super(DetalleProducto, self).get_context_data(**kwargs)
        context['producto_id']=self.kwargs['pk']
        print(context)
        return context
