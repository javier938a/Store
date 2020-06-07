from django.shortcuts import render, redirect
from .models import User, tbl_cliente
from .forms import CreatePerfilCliente, CreateUserForm
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

class index(TemplateView):#Mostrando index Pagina Principal
    template_name ='superStore/index.html'

def register(request):#metodo register sirve para registrar un nuevo usuario
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                do_login(request,user)
                username = form.cleaned_data.get('username')
                url = '/superStore/registrar/perfil/'+username
                return redirect(url)
    return render(request, "superStore/reg_usu.html", {'form':form})



def RegistrarPerfilCliente(request, username):
    if request.method == 'POST':
        print("Funciona")
        formPerfilUser = CreatePerfilCliente(request.POST)
        if formPerfilUser.is_valid():
            print("Funciona")
            formPerfilUser.save()
        return redirect('tienda:index')
    else: 
        formPerfilUser = CreatePerfilCliente()
        print(formPerfilUser.Meta.model.user)
        formPerfilUser.fields['user'].queryset=User.objects.filter(username=username)
        print("esto guarda",User.objects.filter(username=username),formPerfilUser.fields['user'])

    return render(request, 'superStore/reg_perfil_cli.html',{'form':formPerfilUser})
        
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


