from superStore.models import tbl_cliente, User, tbl_cliente, tbl_mayorista
from django.views.generic import DetailView, ListView,TemplateView, UpdateView
from django.shortcuts import render
from superStore.models import tbl_categoria
from superStore.forms import CreatePerfilCliente, CreatePerfilMayorista
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
        tipoUsuario = self.kwargs['pk']#Obteniendo el tipo de usuario de la url
        print("Algo da")
        print(type(self.kwargs['pk']))
        perfil = None # creando variable perfil para almacenar perfil
        if tipoUsuario==1:#Verificando si es Cliente para registrar el perfil del cliente
            perfil_cliente = tbl_cliente.objects.get(user=self.request.user.id)
            context['perfil_cliente']=perfil_cliente
        elif tipoUsuario==2:#Verificando si es Proveedor para registrar el perfil del proveedor
            perfil_proveedor = tbl_mayorista.objects.get(user=self.request.user.id)#pk es el id del usuario
            context['perfil_proveedor']=perfil_proveedor
        
         # agregando el perfil al contexto
        return context
#Metodo para subir archivo recibe como parametro la imagen en bit recogida por el request.FILES.get('foto_perfil')
def subir_image(image_bit, tipo_usuario, imagen_name="img.jpg" ):
    raiz = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    print("Valor de la la raiz de la carpeta")
    print(raiz)
    if tipo_usuario=="Cliente":
        ubi_writer=raiz+"/media/fotoPerfilCliente/"+imagen_name
    else:
        ubi_writer = raiz+"/media/foto_perfil_proveedor/"+imagen_name

    with open(ubi_writer,'wb+') as ubicasion:
        for bin in image_bit.chunks():
            ubicasion.write(bin)
#Fin del metodo de subir imagen

class EditarInformacionPerfilCliente(UpdateView):#vista para editar la informacion del perfil del cliente
    template_name = 'superStore/perfil_usuario/editar_perfil_usuario.html'
    form_class = CreatePerfilCliente
    context_object_name = 'form'
    model = tbl_cliente
    def post(self, request, *args, **kwargs):
        #datos del username#
        nombres = request.POST.get('first_name')
        apellidos = request.POST.get('last_name')
        email = request.POST.get('email')
        #Datos del perfil#
        hay_foto = False
        if request.FILES.get('foto_perfil') is not None:#Verificando si se ha subido foto en el file si hay foto se pocede a guardar la foto
            hay_foto=True #si hay foto la variable cambia a True
            print(type(request.FILES.get('foto_perfil')))
            foto_perfil = request.FILES['foto_perfil']
            subir_image(request.FILES.get('foto_perfil'),"Cliente", str(foto_perfil))#subiendo el archivo a la pagina
            print(foto_perfil)
        genero = request.POST['genero']#Obteniendo genero
        telefono = request.POST['telefono']#Obtenetiendo telefono
        fecha_nacimiento = request.POST['fecha_nacimiento']
        #Realizando la actualizacion de los datos del usuario
        update_user = User.objects.filter(id=request.user.id).update(first_name=nombres, last_name=apellidos, email=email)
        print(update_user)
        print("Varificar: "+str(hay_foto))
        #Si hay foto se procede a realizar la actualizacion
        if hay_foto:
            print("Hola Hay foto")
            update_info = tbl_cliente.objects.filter(id=self.kwargs['pk']).update(foto_perfil=('fotoPerfilCliente/'+str(foto_perfil)), genero=genero, telefono=telefono, fecha_nacimiento=fecha_nacimiento)#actualizando datos
            print(update_info)
        else:
            print("No Hay Foto")
            update_info = tbl_cliente.objects.filter(id=self.kwargs['pk']).update(genero=genero, telefono=telefono, fecha_nacimiento=fecha_nacimiento)#actualizando datos
        
        return redirect('tienda:index')

    def get(self, request, *args, **kwargs):
        print("Holaaaa")
        cliente = tbl_cliente.objects.get(id=self.kwargs['pk'])
        usuario = User.objects.get(username=cliente.user)
        print(usuario)
        return render(request, self.template_name, context={'id_cliente':self.kwargs['pk'],'cliente':cliente,'Usuario':usuario,})    


class EditarInformacionPerfilProveedor(UpdateView):
    template_name = "superStore/perfil_usuario/editar_perfil_proveedor.html"
    form_class = CreatePerfilMayorista
    model = tbl_mayorista

    def get(self, request, *args, **kwargs):
        proveedor = tbl_mayorista.objects.get(id=self.kwargs['pk'])#obteniendo el proveedor del la tabla mayorista
        usuario = User.objects.get(id=proveedor.user.id)#obteniendo el usuario de la tabla User cuyo proveedor sea el de el ID ingresado
        return render(
            request,
            self.template_name,
            context={'id_proveedor':self.kwargs['pk'],
                     'proveedor':proveedor,
                    'usuario':usuario}
                    )
    def post(self, request, *args, **kwars):
        #campos de usuario
        first_name = request.POST.get('nombres')
        last_name = request.POST.get('apellidos')
        email = request.POST.get('correo')
        #campos de perfil proveedor
        hay_foto = False
        foto_perfil = request.FILES.get('foto_perfil')
        if foto_perfil is not None:
            hay_foto=True
            subir_image(foto_perfil,"Proveedor", str(foto_perfil))#metodo que sirve para guardar la imagen recibe la imagen por el metodo request.FILES y el segundo paramentro define si es cliente o proveedor y el tercer parametro el nombre de la imagen
        
        objetivo = request.POST.get('objetivo')
        genero = request.POST.get('genero')
        nombre_empresa = request.POST.get('nombre_empresa')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        #Direccion
        pais = request.POST.get('pais')
        departamento = request.POST.get('departamento')
        municipio = request.POST.get('municipio')
        barrio_canton = request.POST.get('barrio_canton')
        #barrio_canton es barrio_caton en la tabla tbl_mayorista
        update_usuario = User.objects.filter(id=request.user.id).update(
            first_name=first_name,
            last_name = last_name,
            email=email
        )
        if hay_foto:
            update_proveedor = tbl_mayorista.objects.filter(id=self.kwargs['pk']).update(
                foto_perfil=("foto_perfil_proveedor/"+str(foto_perfil)),
                objetivo=objetivo,
                genero=genero,
                nombre_empresa=nombre_empresa,
                telefono=telefono,
                fecha_nacimiento=fecha_nacimiento,
                pais=pais,
                departamento=departamento,
                municipio=municipio,
                barrio_caton=barrio_canton
            )
        else:
            update_proveedor = tbl_mayorista.objects.filter(id=self.kwargs['pk']).update(
                objetivo=objetivo,
                genero=genero,
                nombre_empresa=nombre_empresa,
                telefono=telefono,
                fecha_nacimiento=fecha_nacimiento,
                pais=pais,
                departamento=departamento,
                municipio=municipio,
                barrio_caton=barrio_canton
            )
        return redirect("tienda:index")
