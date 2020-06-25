from superStore.models import tbl_cliente, User, tbl_cliente, tbl_mayorista
from django.views.generic import DetailView, ListView,TemplateView, UpdateView
from django.shortcuts import render
from superStore.models import tbl_categoria
from superStore.forms import CreatePerfilCliente
from django.urls import reverse
from superStore.models import tbl_direccion
 
class UsuarioDetalle(DetailView):
    model = User
    template_name = 'superStore/perfil_usuario/perfil.html'
    context_object_name='form'
    def get_context_data(self, **kwargs):
        context = super(UsuarioDetalle, self).get_context_data(**kwargs)
        tipoUsuario = self.kwargs['tipo_usuario']
        perfil = None # creando variable perfil para almacenar perfil
        if tipoUsuario=='Cliente':#Verificando si es Cliente para registrar el perfil del cliente
            perfil_cliente = tbl_cliente.objects.get(user=self.kwargs['pk'])
            context['perfil_cliente']=perfil_cliente
        elif tipoUsuario=='Proveedor':#Verificando si es Proveedor para registrar el perfil del proveedor
            perfil_proveedor = tbl_mayorista.objects.get(user=self.kwargs['pk'])
            context['perfil_proveedor']=perfil_proveedor
         # agregando el perfil al contexto
        print(self.kwargs['pk'])
        return context

class EditarInformacionPerfil(UpdateView):
    template_name = 'superStore/perfil_usuario/editar_perfil_usuario.html'
    form_class = CreatePerfilCliente
    context_object_name = 'form'
    model = tbl_cliente
    def get_context_data(self, **kwargs):
        context = super(EditarInformacionPerfil,self).get_context_data(**kwargs)
        context.get('form').fields['user'].queryset = tbl_cliente.objects.filter(id = self.kwargs['pk'])
        return context

    
    def get_success_url(self):
        return reverse("tienda:index")
