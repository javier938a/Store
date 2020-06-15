from superStore.models import tbl_venta, tbl_cliente
from superStore.forms import FormCrearVenta
from django.views.generic import CreateView, ListView

class RegistrarVenta(CreateView):
    template_name = 'superStore/procesos_venta/registrar_venta.html'
    context_object_name = 'form'
    form_class = FormCrearVenta
    success_url = '/'
    def get_context_data(self, **kwargs):
        context = super(RegistrarVenta, self).get_context_data(**kwargs)
        context.get('form').fields['cliente_id'].queryset = tbl_cliente.objects.filter(id=self.kwargs['pk'])
        return context
    
class ListarVenta(ListView):
    context_object_name = 'venta_list'
    model = tbl_venta
    template_name = 'superStore/procesos_venta/listar_venta.html'
    success_url ='/'

    def get_queryset(self):
        print("Esto imprime")
        print(self.kwargs['pk'])
        return tbl_venta.objects.filter(producto_id__mayorista=self.kwargs['pk'])#filtrando que solo se muestren las ventas realizada de un determinado proveedor que se especifica con su pk id respectivamente 
