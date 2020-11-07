from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from superStore.forms import ProveedorForm
from superStore.models import tbl_proveedor, tbl_mayorista
class RegistrarProveedor(CreateView):
    template_name='superStore/proces_proveedor/registrar_proveedor.html'
    form_class=ProveedorForm
    model=tbl_proveedor

    def get_context_data(self, **kwargs):
        context=super(RegistrarProveedor, self).get_context_data(**kwargs)
        context.get('form').fields.get('mayorista').empty_label=None
        context.get('form').fields.get('mayorista').queryset=tbl_mayorista.objects.filter(user__id=self.request.user.id)
        return context
    
    def get_success_url(self):
        return reverse_lazy('tienda:listar_proveedores')
    

class ListarProveedores(ListView):
    model=tbl_proveedor
    template_name='superStore/proces_proveedor/listar_proveedores.html'
    context_object_name='proveedores'

    def get_queryset(self):
        clave=self.request.GET.get('txt_clave_prove')
        print('esta es la clave: '+str(clave))
        if clave is not None:
            return self.model.objects.filter(Q(empresa__icontains=clave)|Q(representante__icontains=clave)|Q(contacto=clave)|Q(direccion__icontains=clave) & Q(mayorista__user__id=self.request.user.id))
        
        return self.model.objects.filter(Q(mayorista__user__id=self.request.user.id))


class EditarProveedor(UpdateView):
    template_name='superStore/proces_proveedor/registrar_proveedor.html'
    form_class=ProveedorForm
    model=tbl_proveedor

    def get_context_data(self, **kwargs):
        context=super(EditarProveedor, self).get_context_data(**kwargs)
        context.get('form').fields.get('mayorista').empty_label=None
        context.get('form').fields.get('mayorista').queryset=tbl_mayorista.objects.filter(user__id=self.request.user.id)
        return context
    
    def get_success_url(self):
        return reverse_lazy('tienda:listar_proveedores')

class EliminarProveedor(DeleteView):
    template_name='superStore/proces_proveedor/eliminar_proveedor.html'
    model=tbl_proveedor
    context_object_name='prove'
    success_url=reverse_lazy('tienda:listar_proveedores')