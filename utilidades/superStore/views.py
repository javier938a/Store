from django.shortcuts import render, redirect
from .models import User, tbl_tipo_usuario, tbl_pais, tbl_cliente, tbl_mayorista
from .forms import CreatePerfilCliente, CreateUserForm, CreatePerfilMayorista
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

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
    return render(request, "superStore/registrar/reg_usu.html", {'form':form})



def RegistrarPerfilCliente(request, username, tipo_usuario):
    form = None
    if request.method == 'POST':
        print("Funciona")
        if tipo_usuario=='Cliente':
            form = CreatePerfilCliente(request.POST)
            registrar_perfil(form)#llamada al metodo registrar perfil para registrar el perfil del usuario
            return redirect('tienda:index')
        elif  tipo_usuario=='Proveedor':
            form = CreatePerfilMayorista(request.POST)
            registrar_perfil(form)
            return redirect('tienda:index')
    else: 
        if tipo_usuario == 'Cliente':#verificando si el usuario es cliente para pintar el formulario del cliete
            form = CreatePerfilCliente()
            print(form.Meta.model.user)
            form['user'].queryset=User.objects.filter(username=username)
            print("esto guarda",User.objects.filter(username=username),form.fields['user'])
        elif tipo_usuario=='Proveedor':
            form = CreatePerfilMayorista()#verificand si el usuario es proveedor para pintar el formulario del proveedor en la plantilla
            form.fields['user'].queryset = User.objects.filter(username=username)

    return render(request, 'superStore/registrar/reg_perfil_cli.html',{'form':form})

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
            'superStore/registrar/login.html',
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