from superStore.models import tbl_cliente, User, tbl_cliente, tbl_mayorista
from django.views.generic import DetailView, ListView,TemplateView, UpdateView
from django.shortcuts import render
from superStore.models import tbl_categoria
from superStore.forms import CreatePerfilCliente
from django.urls import reverse, reverse_lazy
from superStore.models import tbl_direccion
from django.shortcuts import redirect
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
import urllib
import os
 
class UsuarioDetalle(DetailView):
    model = User
    template_name = 'superStore/perfil_usuario/perfil.html'
    context_object_name='form'
    def get_context_data(self, **kwargs):
        context = super(UsuarioDetalle, self).get_context_data(**kwargs)
        tipoUsuario = self.kwargs['tipo_usuario']#Obteniendo el tipo de usuario de la url
        perfil = None # creando variable perfil para almacenar perfil
        if tipoUsuario=='Cliente':#Verificando si es Cliente para registrar el perfil del cliente
            perfil_cliente = tbl_cliente.objects.get(user=self.kwargs['pk'])
            context['perfil_cliente']=perfil_cliente
        elif tipoUsuario=='Proveedor':#Verificando si es Proveedor para registrar el perfil del proveedor
            perfil_proveedor = tbl_mayorista.objects.get(user=self.kwargs['pk'])#pk es el id del usuario
            context['perfil_proveedor']=perfil_proveedor
         # agregando el perfil al contexto
        print(self.kwargs['pk'])
        return context

def subir_archivo(image_bit, imagen_name="img.jpg"):
    raiz = os.path.join(os.path.dirname(os.path.dirname(__file__))).replace('/superStore','')
    with open((raiz+"/media/fotoPerfilCliente/"+imagen_name+""),"wb+") as ubicasion:
        print("heloooo")
        print(ubicasion)
        for bin in image_bit.chunks():
            ubicasion.write(bin)
class EditarInformacionPerfil(UpdateView):
    template_name = 'superStore/perfil_usuario/editar_perfil_usuario.html'
    form_class = CreatePerfilCliente
    context_object_name = 'form'
    model = tbl_cliente
    def post(self, request, *args, **kwargs):
        print("Valor de file")
        print(type(request.FILES.get('foto_perfil')))
        foto_perfil = request.FILES['foto_perfil']
        subir_archivo(request.FILES.get('foto_perfil'), str(foto_perfil))#subiendo el archivo a la pagina
        print(str(foto_perfil))
        genero = request.POST['genero']
        telefono = request.POST['telefono']
        fecha_nacimiento = request.POST['fecha_nacimiento']
        update_info = tbl_cliente.objects.filter(id=self.kwargs['pk']).update(foto_perfil=foto_perfil, genero=genero, telefono=telefono, fecha_nacimiento=fecha_nacimiento)#actualizando datos
        print(update_info)
        
        return redirect('tienda:index')

    def get(self, request, *args, **kwargs):
        print("Holaaaa")
        cliente = tbl_cliente.objects.get(id=self.kwargs['pk'])
        print(cliente.foto_perfil)
        return render(request, self.template_name, context={'id_cliente':self.kwargs['pk'],'cliente':cliente})    
    
    def get_success_url(self):
        return reverse("tienda:index")
