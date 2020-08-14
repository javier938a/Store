from django.shortcuts import render, redirect
from .models import User, tbl_tipo_usuario, tbl_pais, tbl_cliente, tbl_mayorista, tbl_direccion, tbl_producto
from .forms import CreatePerfilCliente, CreateUserForm, CreatePerfilMayorista, FormCrearDireccion, FormCrearProducto
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model#obtiene el modelo de usuario personalizado
from django.contrib.auth.backends import ModelBackend#Obteniendo el modelo backend
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from .proces_venta.crud_venta import RegistrarVenta, ListarVenta #importanto la clase de registrar Venta
from .proces_producto.crud_producto import RegistrarProducto, ListarProductos, EditarProducto, EliminarProducto, DetalleProducto, buscar_producto_tienda, cargar_todos_productos_tienda #todos los procesos de producto
from .proces_cesta.crud_cesta import ListarCesta, Agregar_a_Cesta, ActualizarCesta, EliminarCesta# importando la clase listar cesta en donde me lista todos productos de la cesta
from .models import tbl_categoria, tbl_sub_categoria1
from .forms import FormCrearDireccion
from django.db import DatabaseError, transaction
from .inicio.inicio_usuario import UsuarioDetalle # este modulo se usara para cuando la persona inicie secion
from .inicio.inicio_usuario import EditarInformacionPerfilCliente, EditarInformacionPerfilProveedor
from django.contrib.auth.mixins import LoginRequiredMixin
from .proces_venta.crud_venta import ModificarEstadoEnvio
from .proces_venta.crud_venta import EliminarVenta
from .proces_comentario.crud_comentario import EscribirComentario, EliminarComentario, listarComentarios, EditarComentar
from .proces_seguidores.crud_seguidores import verificar_existe_seguidor, agregar_nuevo_seguidor#metodo que verificara si existen seguidores
from django.db.models import Q
from .models import tbl_seguidores
from django.utils import timezone
import datetime
from django.db.models.functions import Extract
from superStore.notificaciones.notif import guardar_token
from .proces_favoritos.crud_favoritos import aniadir_favoritos
from .proces_favoritos.crud_favoritos import listarFavoritos #Listar favoritos
from .proces_categoria.crud_categoria import listarCategoria, listarSubCategoria1
from .proces_ubicacion.crud_ubicacion import ListarPais, ListarDepartamentos, ListarMunicipio, ListarBCanton
from .forms import FormDireP
from .inicio.inicio_usuario import listarDeptoA, listarMuniA, listarBacanA
# Create your views here.
class index(ListView):#Mostrando index Pagina Principal
    #login_url ='tienda:login'
    #redirect_field_name='redirect_to'
    template_name ='superStore/index.html'
    model = tbl_categoria
    context_object_name='cate_list'
    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        user = self.request.user
        id_cli = self.request.session.get('id_cli',0)
        clave = self.request.GET.get('clave')#busqueda por clave de busqueda..
        id_Subcategoria = self.request.GET.get('id_sub')#buscando por subcategoria..
        id_boc = self.request.GET.get('boc')#id barrio o canton
        id_pais = self.request.GET.get('id_pais')#buscar por departamento
        id_depto=self.request.GET.get('id_depto')#Buscar por municipio
        id_muni=self.request.GET.get('id_muni')
        print(id_pais)
        id_prove = self.request.session.get('id_prove', 0)
        paises = tbl_pais.objects.all()#obteniendo el listado de todos los
        context['paises']=paises
        print("Esta es la clave "+str(clave))
        if user.is_authenticated:#Verifica si el usuario esta autenticado
            pass
            print("El Valor de request.user")
            if user.tipo_usuario_id.tipo_usuario =="Cliente":#verifica si es cliente
                if tbl_cliente.objects.filter(user=user).exists():#si el usuario esta en la tabla cliente significa que tiene perfil registrado
                    id_cli = tbl_cliente.objects.get(user=user).id#Verifica si se a creado el perfil del cliente no existe hay que crearlo
                    self.request.session['id_cli']=id_cli
                    context['id_cli']=id_cli #agrega al contexto el id del cliente
            else:
                if tbl_mayorista.objects.filter(user=user).exists():
                    id_prove = tbl_mayorista.objects.get(user=user).id#obtiene el id del mayorista en dado caso sea mayorista
                    self.request.session['id_prove']=id_prove#agregar a sesion la variable id_prove
                    context['id_prove'] = id_prove #agrega al contexto el id del proveedor
                    #Obteniendo el listado de notificaciones de nuevos seguidores
                    '''fecha = timezone.now()
                    fecha_hoy = fecha.date()
                    dia = fecha_hoy.day-7#Restandole 7 dias para que sea la semana pasada
                    mes = fecha_hoy.month
                    anio = fecha_hoy.year
                    fecha_sem_pas = datetime.date(anio, mes,dia)
                    noti_seguir = tbl_seguidores.objects.filter(Q(mayorista=id_prove) & Q(fecha_de_seguidor__range=[fecha_sem_pas,fecha_hoy]))
                    print(noti_seguir)
                    context['noti_seguidores']=noti_seguir'''
        print(clave)
        print("id de la subCategoria")
        print(id_Subcategoria)
        if id_muni is not None:
            context['producto']=tbl_producto.objects.filter(Q(mayorista__barrio_canton__municipio__id=id_muni))
        else:
            if id_depto is not None:
                context['producto']=tbl_producto.objects.filter(Q(mayorista__barrio_canton__municipio__departamento__id=id_depto))
            else:
                if id_pais is not None:
                    context['producto']=tbl_producto.objects.filter(Q(mayorista__barrio_canton__municipio__departamento__pais__id=id_pais))
                else:
                    if id_boc is not None:
                        context['producto']=tbl_producto.objects.filter(Q(mayorista__barrio_canton__id=id_boc))
                    else:
                        if id_Subcategoria is not None:
                            context['producto']=tbl_producto.objects.filter(Q(sub_categoria1__id=id_Subcategoria))
                        else:
                            if clave==None:#se verifica que exista clave si no existe se muestran todos
                                print("Esta es la clave!")
                                context['producto']=tbl_producto.objects.all()
                            else:
                                context['producto']=tbl_producto.objects.filter(Q(producto__icontains=clave))
                

            
    
        #print('Valores')
       # print(context.get('cate_list'))
        return context


class ListarSubCategoria(ListView):
    template_name = "superStore/proces_categoria/listar_sub_categoria.html"
    model = tbl_sub_categoria1
    context_object_name = 'listar_sub_categoria'
    def get_queryset(self):
        return tbl_sub_categoria1.objects.filter(categoria=self.kwargs['pk'])


def register(request):#metodo register sirve para registrar un nuevo usuario
    form = CreateUserForm()#Creando un formulario vario de Registro de Usuario
    if request.method == "POST":#verificando si se ha revivido una peticion por el metodo post
        form = CreateUserForm(data=request.POST)#asignando los datos enviados a travez del metodo post
        print(form.is_valid())
        if form.is_valid():# si el formulario es valido
            form.save()#Guardar formulario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            print(str(username)+' '+str(password))
            user = authenticate(username=username, password=password)#Autenticando el usuario
            #user = User.objects.get(username=username)#obteniendo una instancia del usuario recien registrado
            print("Valor de user:")
            print(user)
            #print(retorno)
            if user is not None:
                do_login(request,user) #Logiando al usuario al sistema
                tipo = request.user.tipo_usuario_id.tipo_usuario #
            
                url = None
                if str(tipo) == "Cliente":#Verificando si el usuario es cliente o proveedor para si establecer su url
                    url = 'tienda:perfil_cli'
                    print("Entro al url"+url)
                elif str(tipo) == "Proveedor":
                    url = 'tienda:reg_provee'
                return redirect(url)
    return render(request, "superStore/registrar_usuario/reg_usu.html", {'form':form})
def logiar(request):
    #Creamos el formulario de autenticacion vacio
    form = AuthenticationForm()
    if request.method == 'POST':
        #Añadimos los datos recibidos
        form = AuthenticationForm(data=request.POST)
        #si el formulario es valido
        if form.is_valid():
            #recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            #verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)
            print("este es el login")
            print(user)
            #si existe un usuario con ese nombre y contraseña 
            if user is not None:
                if user.is_active:
                    #hacemos rastreamos el usuario logeado
                    do_login(request, user)
                    #redireccioamos a la portada
                    #url = '/superStore/'+str(usuario.id)
                    return redirect('tienda:index')
        #Si llegamos al final renderizamos el formulario
    return render(
            request,
            'superStore/registrar_usuario/login.html',
            { 'form':form }
        )

#Creando el formulario de informacion del usuario

# aqui se definiria el logout 
def logout_user(request):
    logout(request)
    template = 'superStore/registrar_usuario/logout.html'
    return render(request, template)

def RegistrarPerfilCliente(request):
    form = None
    if request.method == 'POST':
        print("Funciona")
        form = CreatePerfilCliente(request.POST, request.FILES)
        s = form.is_valid()
        print("¿Funcionara?")
        print(s)
        #print(form.errors)
        if form.is_valid():
            form.save()
            id_cliente = tbl_cliente.objects.get(user__id=request.user.id).id
            print(id_cliente)
            url ='/superStore/registrar/direccion/'+str(id_cliente)
            return redirect(url)
    else:
        form = CreatePerfilCliente()
        #print(form.Meta.model.user)
        form.fields['user'].queryset=User.objects.filter(id=request.user.id)
        #print("esto guarda",User.objects.filter(id=pk),form.fields['user'])

    return render(request, 'superStore/registrar_usuario/reg_perfil_cli.html',{'form':form})

def RegistrarPerfilProveedor(request):
    template = 'superStore/registrar_usuario/reg_perfil_provee.html'
    FormDir=FormDireP()
    print("Aqui---->")
    print(FormDir.is_valid())
    form = None
    if request.method == "POST":
        form = CreatePerfilMayorista(request.POST, request.FILES)
        s=form.is_valid()
        print(form.errors)
        print("esto dice")
        print(s)
        if form.is_valid():
            form.save()
            return redirect("tienda:index")
    else:
        form = CreatePerfilMayorista()
        form.fields['user'].queryset  = User.objects.filter(id=request.user.id)
    
    return render(
        request,
        template,
        context={'form':form,'formDir':FormDir}
    )


class ListarDireccion(ListView):
    template_name ='superStore/registrar_usuario/listar_direccion.html'
    model = tbl_direccion
    context_object_name='dire_list'
    def get_context_data(self, **kwargs):
        context = super(ListarDireccion, self).get_context_data(**kwargs)
        context['id_cliente']=self.kwargs['pk']
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(cliente__id=self.kwargs['pk'])


class RegistrarDireccion(CreateView):#sirve para registrar las direcciones del usuario
    template_name = 'superStore/registrar_usuario/registrar_direccion.html'
    form_class = FormCrearDireccion
    context_object_name = 'form'
    success_url = reverse_lazy('tienda:login')
    def get_context_data(self, **kwargs):
        context = super(RegistrarDireccion, self).get_context_data(**kwargs)
        context.get('form').fields['cliente'].queryset = tbl_cliente.objects.filter(id=self.kwargs['pk'])# validando que solo aparesca el Cliente pueda ingresar direccion
        context['id_cliente']=self.kwargs['pk']
        return context
    
    def form_valid(self, form):
        estado_guardado = form.cleaned_data['estado']
        print(estado_guardado)
        if estado_guardado==True:
            direcciones = tbl_direccion.objects.filter(Q(cliente__user__id=self.request.user.id)).update(estado=False)
            print(direcciones)
        
        form_valid = super(RegistrarDireccion, self).form_valid(form)
        return form_valid


    def get_success_url(self):
        return reverse_lazy('tienda:dire_list', args=[str(self.kwargs['pk'])])

class EditarDireccion(UpdateView):
    template_name = 'superStore/registrar_usuario/editar_direccion.html'
    form_class = FormCrearDireccion
    context_object_name = 'form'
    model = tbl_direccion

    def get_context_data(self, **kwargs):
        context = super(EditarDireccion, self).get_context_data(**kwargs)
        direccion = self.model.objects.get(id=self.kwargs['pk'])
        print("Imprime cliente")
        print(direccion.cliente.id)
        context.get('form').fields['cliente'].queryset = tbl_cliente.objects.filter(id = direccion.cliente.id )
        direccion = self.model.objects.get(id = self.kwargs['pk'])
        context['id_cliente']=direccion.cliente.id
        return context
        
    def form_valid(self, form):
        estado_editado=form.cleaned_data['estado']
        print(estado_editado)
        #verificando si la direccion ingresado, el estado es igual a True
        if estado_editado==True:
            print(self.request.user.id)#si la direccion ingresada es igual a true obtiene los demas registros obviando el que se ha editado y actualiza los demas estados en false
            direcciones = tbl_direccion.objects.filter(~Q(id=self.kwargs['pk']) & Q(cliente__user__id=self.request.user.id)).update(estado=False)
            
            print(direcciones)
        form_valid = super(EditarDireccion, self).form_valid(form)
        print("Esta aqui")
        print(form_valid)
        return form_valid
    def get_success_url(self):
        direccion = self.model.objects.get(id=self.kwargs['pk'])

        #id_cliente = tbl_cliente
        return reverse_lazy('tienda:dire_list', args=[str(direccion.cliente.id)])

class EliminarDireccion(DeleteView):
    template_name = 'superStore/registrar_usuario/eliminar_direccion.html'
    model = tbl_direccion
    context_object_name='delete_dire'
    def get_context_data(self, **kwargs):
        context = super(EliminarDireccion, self).get_context_data(**kwargs)
        print(context)
        return context

    def get_success_url(self):
        direccion = self.model.objects.get(id=self.kwargs['pk'])
        return reverse_lazy('tienda:dire_list', args=[str(direccion.cliente.id)])

class RegistrarProducto(RegistrarProducto):#esta vista sirve para registrar producto se pasa el ID del Mayorista para filtrar que sea el mayorista ingresado
    pass

class ListarProductos(ListarProductos):#clase que sirve para listar productos
    pass

class EditarProducto(EditarProducto):# vista que sirve para editar producto
    pass

class EliminarProducto(EliminarProducto):#Vista que sirve para eliminar producto
    pass 

class RegistrarVenta(RegistrarVenta):#sirve para heredar de registrar venta que esta en el modulo de proces_venta
    pass

class ListarVenta(ListarVenta):#sirve para heredad de Listar venta
    pass
