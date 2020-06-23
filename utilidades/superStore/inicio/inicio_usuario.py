from superStore.models import tbl_cliente, User
from django.views.generic import DetailView, ListView,TemplateView
from django.shortcuts import render
 
class UsuarioDetalle(DetailView):
    model = User
    template_name = 'superStore/perfil_usuario/perfil.html'
    context_object_name='form'
    def get_context_data(self, **kwargs):
        context = super(UsuarioDetalle, self).get_context_data(**kwargs)
        tipoUsuario = self.kwargs['tipo_usuario']
        perfil = None # creando variable perfil para almacenar perfil
        if tipoUsuario=='Cliente':#Verificando si es Cliente para registrar el perfil del cliente
            perfil = tbl_cliente.objects.get(user=self.kwargs['pk'])
        elif tipoUsuario=='Proveedor':#Verificando si es Proveedor para registrar el perfil del proveedor
            perfil = tbl_mayorista.objects.get(user=self.kwargs['pk'])
        context['perfil']=perfil # agregando el perfil al contexto
        print(self.kwargs['pk'])
        print(perfil.pais_id)
        return context

