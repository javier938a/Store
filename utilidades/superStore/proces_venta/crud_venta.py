from superStore.models import tbl_venta, tbl_cliente, tbl_producto
from superStore.forms import FormCrearVenta
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

class RegistrarVenta(CreateView):
    template_name = 'superStore/procesos_venta/registrar_venta.html'
    context_object_name = 'form'
    form_class = FormCrearVenta

    def get_context_data(self, **kwargs):
        context = super(RegistrarVenta, self).get_context_data(**kwargs)
        context.get('form').fields['cliente_id'].queryset = tbl_cliente.objects.filter(id=self.kwargs['pk'])#obteniendo el cliente que va comprar el producto
        context.get('form').fields['producto_id'].queryset = tbl_producto.objects.filter(id=self.kwargs['pk1'])#obteniendo el producto que va comprar el cliente
        context.get('form').initial={'precio_unitario':self.kwargs['precio'],}
        print(context.get('form')['precio_unitario'].value())
        return context
    
    def form_valid(self, form):
        cantidad = form.cleaned_data.get('cantidad')
        precio_unitario = form.cleaned_data.get('precio_unitario')
        total = int(cantidad)*float(precio_unitario)
        form.instance.precio_total = total
        form_valid = super(RegistrarVenta, self).form_valid(form)
        return form_valid

    def get_success_url(self):
        return reverse_lazy('tienda:index')
class ListarVenta(ListView):
    context_object_name = 'venta_list'
    model = tbl_venta
    template_name = 'superStore/procesos_venta/listar_venta.html'

    def get_context_data(self, **kwargs):
        context = super(ListarVenta, self).get_context_data(**kwargs)
        context['pk']=self.kwargs['pk']
        return context

    def get_queryset(self):
        print("Esto imprime")
        print(self.kwargs['pk'])
        return tbl_venta.objects.filter(producto_id__mayorista=self.kwargs['pk'])#filtrando que solo se muestren las ventas realizada de un determinado proveedor que se especifica con su pk id respectivamente 
