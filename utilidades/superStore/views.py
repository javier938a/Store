from django.shortcuts import render, redirect
from .models import User, tbl_tipo_usuario, tbl_pais, tbl_cliente, tbl_mayorista, tbl_direccion, tbl_producto
from .forms import CreatePerfilCliente, CreateUserForm, CreatePerfilMayorista, FormCrearDireccion, FormCrearProducto
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy, reverse

# Create your views here.

class index(TemplateView):#Mostrando index Pagina Principal
    template_name ='superStore/index.html'

def register(request):#metodo register sirve para registrar un nuevo usuario
    form = CreateUserForm()#Creando un formulario vario de Registro de Usuario
    if request.method == "POST":#verificando si se ha revivido una peticion por el metodo post
        form = CreateUserForm(data=request.POST)#asignando los datos enviados a travez del metodo post
        print(form.is_valid())
        if form.is_valid():# si el formulario es valido
            user = form.save()#Guardar formulario
            print(user)
            if user is not None:
                do_login(request,user) 
                username = form.cleaned_data.get('username')
                tipo_usuario = form.cleaned_data.get('tipo_usuario_id')
                print('valor: '+str(tipo_usuario))
                url = '/superStore/registrar/perfil_reg/'+str(username)+'/'+str(tipo_usuario)
                return redirect(url)
    return render(request, "superStore/registrar_usuario/reg_usu.html", {'form':form})



def RegistrarPerfilCliente(request, username, tipo_usuario):
    form = None
    if request.method == 'POST':
        print("Funciona")
        if tipo_usuario=='Cliente':
            form = CreatePerfilCliente(request.POST)
            registrar_perfil(form)#llamada al metodo registrar perfil para registrar el perfil del usuario
            usuario = User.objects.get(username=username)

            cliente  = tbl_cliente.objects.get(user=usuario.id)
            print("hhhaaaaa")
            print(cliente.id)
            url='/superStore/registrar/direccion/'+str(cliente.id)
            return redirect(url)
        elif  tipo_usuario=='Proveedor':
            form = CreatePerfilMayorista(request.POST)
            registrar_perfil(form)
            return redirect('tienda:index')
    else: 
        if tipo_usuario == 'Cliente':#verificando si el usuario es cliente para pintar el formulario del cliete
            form = CreatePerfilCliente()
            print(form.Meta.model.user)
            form.fields['user'].queryset=User.objects.filter(username=username)
            print("esto guarda",User.objects.filter(username=username),form.fields['user'])
        elif tipo_usuario=='Proveedor':
            form = CreatePerfilMayorista()#verificand si el usuario es proveedor para pintar el formulario del proveedor en la plantilla
            form.fields['user'].queryset = User.objects.filter(username=username)

    return render(request, 'superStore/registrar_usuario/reg_perfil_cli.html',{'form':form})

def registrar_perfil(form):#Funcion que servira para guardar formulario
    if form.is_valid():
        form.save()  

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

            #si existe un usuario con ese nombre y contraseña 
            if user is not None:
                #hacemos el login manualmente
                do_login(request, user)
                
                #redireccioamos a la portada
                return redirect('/')
        #Si llegamos al final renderizamos el formulario
    return render(
            request,
            'superStore/registrar_usuario/login.html',
            { 'form':form }
        )

#Creando el formulario de informacion del usuario

class UsuarioDetalle(DetailView):
    model = User
    template_name = 'info/perfil.html'
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
class RegistrarDireccion(CreateView):#sirve para registrar las direcciones del usuario
    template_name = 'superStore/registrar_usuario/registrar_direccion.html'
    form_class = FormCrearDireccion
    context_object_name = 'form'
    success_url = reverse_lazy('tienda:login')
    def get_context_data(self, **kwargs):
        context = super(RegistrarDireccion, self).get_context_data(**kwargs)
        context.get('form').fields['cliente'].queryset = tbl_cliente.objects.filter(id=self.kwargs['pk'])# validando que solo aparesca el Cliente pueda ingresar direccion
        return context

class RegistrarProducto(CreateView):#esta vista sirve para registrar producto se pasa el ID del Mayorista para filtrar que sea el mayorista ingresado
    template_name = 'superStore/procesos_producto/registrar_productos.html'
    form_class = FormCrearProducto
    context_object_name = 'form'
    success_url='/'
    def get_context_data(self,**kwargs):
        context = super(RegistrarProducto, self).get_context_data(**kwargs)
        context.get('form').fields['mayorista'].queryset = tbl_mayorista.objects.filter(id=self.kwargs['pk'])#Validando que solo el mayorista que ha ingresado seccion vea sus productos en inventario
        return context


class ListarProductos(ListView):
    template_name = 'superStore/procesos_producto/listar_productos.html'
    model = tbl_producto
    context_object_name = 'prod_list'
    
    def get_queryset(self):
        return self.model.objects.filter(mayorista=self.kwargs['pk'])#filtrando que solo sean los productos del mayorista que acaba de iniciar secion sean los que se vean

class EditarProducto(UpdateView):
    template_name = 'superStore/procesos_producto/registrar_productos.html'
    form_class = FormCrearProducto
    model = tbl_producto
    context_object_name = 'form'
    
    def get_context_data(self, **kwargs):
        context = super(EditarProducto, self).get_context_data(**kwargs)
        context['editar']=1 #servira para validar si se esta usando para registrar o editar
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
        context['producto'] = self.get_object()#agrego 
        print("Esto es")
        print(self.get_object().mayorista.id)
        return context
    #el metodo get_object() obtiene el objeto del get_queryset() el objeto espeficio seleccionado
    def get_success_url(self):
        return reverse_lazy('tienda:listar_prod', args=[str(self.get_object().mayorista.id)])
    