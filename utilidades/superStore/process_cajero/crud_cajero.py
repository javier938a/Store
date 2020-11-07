from django.http import request
from superStore.models import tbl_mayorista
from superStore.models import User
from django.db import models
from superStore.models import tbl_cajero, tbl_caja, tbl_tipo_usuario
from superStore.forms import CajeroForm, CreateUserForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
class RegistrarUserCajero(CreateView):
    #se usara el mismo template que se usa al registrarse por primera vez
    template_name='superStore/registrar_usuario/reg_usu.html'
    form_class=CreateUserForm
    usuario=''

    def get_context_data(self, **kwargs):
        context=super(RegistrarUserCajero, self).get_context_data(**kwargs)
        context.get('form').fields.get('tipo_usuario_id').empty_label=None
        context.get('form').fields.get('tipo_usuario_id').queryset=tbl_tipo_usuario.objects.filter(tipo_usuario='cajero')
        return context

    def get_success_url(self):
        cajero=User.objects.get(id=self.object.id)
        print(cajero)
        return reverse_lazy('tienda:registrar_cajero', args=[str(cajero.id)])



class RegistrarCajero(CreateView):
    template_name='superStore/proces_cajero/registrar_cajero.html'
    form_class=CajeroForm
    context_object_name='form'
    
    def get_context_data(self, **kwargs):
        context=super(RegistrarCajero, self).get_context_data(**kwargs)
        context.get('form').fields.get('mayorista').empty_label=None
        context.get('form').fields.get('mayorista').queryset=tbl_mayorista.objects.filter(user__id=self.request.user.id)
        context.get('form').fields.get('user').empty_label=None
        context.get('form').fields.get('user').queryset=User.objects.filter(id=self.kwargs['pk'])
        context.get('form').fields.get('cajero').empty_label=None
        context.get('form').fields.get('cajero').queryset=tbl_caja.objects.filter(mayorista__user__id=self.request.user.id)
        return context
    
    def get_success_url(self):
        return reverse_lazy('tienda:listar_cajeros')

class ListarCajeros(ListView):
    template_name='superStore/proces_cajero/listar_cajeros.html'
    model=tbl_cajero
    context_object_name='cajeros'

    def get_queryset(self):
        clave=self.request.GET.get('txt_clave_cajero')
        if clave is not None:
            return tbl_cajero.objects.filter(Q(mayorista__user__id=self.request.user.id) & Q(cajero__caja__icontains=clave)|Q(user__username__icontains=clave)|Q(user__first_name__icontains=clave)|Q(user__last_name__icontains=clave)|Q(dui__icontains=clave)|Q(telefono=clave)|Q(direccion__icontains=clave))

        return tbl_cajero.objects.filter(mayorista__user__id=self.request.user.id)


class EditarUserCajero(UpdateView):
    template_name='superStore/registrar_usuario/reg_usu.html'
    form_class=CreateUserForm
    model=User

    def get_context_data(self, **kwargs):
        context=super(EditarUserCajero, self).get_context_data(**kwargs)
        context.get('form').fields.get('tipo_usuario_id').empty_label=None
        context.get('form').fields.get('tipo_usuario_id').queryset=tbl_tipo_usuario.objects.filter(tipo_usuario='cajero')
        return context
    
    def get_success_url(self):
    
        username=self.request.POST.get('username')

        cajero=tbl_cajero.objects.get(user__id=self.kwargs['pk'])
        print("Esto dice...")
        print(self.get_object())
        print(cajero)
        print(cajero.id)
        print(self.kwargs)

        return reverse_lazy('tienda:editar_cajero', args=[str(cajero.id)])

class EditarCajero(UpdateView):
    template_name='superStore/proces_cajero/registrar_cajero.html'
    form_class=CajeroForm
    context_object_name='form'
    model=tbl_cajero
    def get_context_data(self, **kwargs):
        context=super(EditarCajero, self).get_context_data(**kwargs)
        context.get('form').fields.get('mayorista').empty_label=None
        context.get('form').fields.get('mayorista').queryset=tbl_mayorista.objects.filter(user__id=self.request.user.id)
        context.get('form').fields.get('user').empty_label=None

        context.get('form').fields.get('user').queryset=User.objects.filter(id=self.get_object().user.id)
        context.get('form').fields.get('cajero').empty_label=None
        context.get('form').fields.get('cajero').queryset=tbl_caja.objects.filter(mayorista__user__id=self.request.user.id)
        return context
    
    def get_success_url(self):
        return reverse_lazy('tienda:listar_cajeros')


class EliminarCajero(DeleteView):
    template_name='superStore/proces_cajero/eliminar_cajero.html'
    model=tbl_cajero

    def get_success_url(self):
        user_cajero_del=User.objects.filter(id=self.kwargs['pk']).delete()
        print('Usuario Eliminado..')
        print(user_cajero_del)
        
        return reverse_lazy('tienda:listar_cajeros')


