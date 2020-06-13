from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, tbl_mayorista, tbl_cliente, tbl_direccion, tbl_producto

class CreateUserForm(UserCreationForm):#extienda de la clase UserCreationForm
   class Meta:
        model = User
        fields = ('username','email', 'first_name','last_name','tipo_usuario_id')
        labels={
            'username':'Nombre de Usuario',
            'email':'Correo',
            'first_name':'Nombres',
            'last_name':'Apellidos',
            'tipo_usuario_id':'Tipo de Usuario',
        }
class CreatePerfilCliente(forms.ModelForm):#Registra el perfil del cliente
    class Meta:
        model = tbl_cliente
        fields = ('user','genero','nombre_negocio','telefono','pais_id','fecha_nacimiento')
        labels = {
            'user':'Usuario',
            'genero':'Genero',
            'nombre_negocio':'Nombre del negocio',
            'telefono':'Telefono',
            'pais_id':'Pais',
            'fecha_nacimiento':'Fecha de nacimiento',
        }
        widgets={
            'user':forms.Select(attrs={'class':'form-control'}),
            'genero':forms.Select(attrs={'class':'form-control'}),
            'nombre_negocio':forms.TextInput(attrs={'class':'form-control'}),
            'telefono':forms.DateInput(attrs={'class':'form-control'}),
            'pais_id':forms.Select(attrs={'class':'form-control'}),
            'fecha_nacimiento':forms.TextInput(attrs={'class':'form-control'}),
        }

class CreatePerfilMayorista(forms.ModelForm):#Registra el perfil del proveedor
    class Meta:
        model = tbl_mayorista
        fields = ('user','genero','nombre_empresa','telefono','pais_id','fecha_nacimiento','direccion')
        labels = {
            'user':'Usuario',
            'genero':'Genero',
            'nombre_empresa':'Empresa',
            'telefono':'Telefono',
            'pais_id':'Pais',
            'fecha_nacimiento':'Fecha de nacimiento',
            'direccion':'Direccion de la empresa',
        }
        widgets={
            'user':forms.Select(attrs={'class':'form-control'}),
            'genero':forms.Select(attrs={'class':'form-control'}),
            'nombre_empresa':forms.TextInput(attrs={'class':'form-control'}),
            'telefono':forms.TextInput(attrs={'class':'form-control'}),
            'pais_id':forms.Select(attrs={'class':'form-control'}),
            'fecha_nacimiento':forms.DateInput(attrs={'class':'form-control'}),
            'direccion':forms.TextInput(attrs={'class':'form-control'}),
        } 

class FormCrearDireccion(forms.ModelForm):#para registrar las multiples direcciones que pueda tener un cliente
    class Meta:
        model = tbl_direccion
        fields = ('cliente','direccion','estado')  
        labels = {
            'cliente':'Cliente',
            'direccion':'Direccion',
            'estado':'Asignar a direccion actual',
        }
        widgets= {
            'cliente':forms.Select(attrs={'class':'form-control'}),
            'direccion':forms.TextInput(attrs={'class':'form-control'}),
            'estado':forms.CheckboxInput(attrs={'class':'form-control'}),
        }

class FormCrearProducto(forms.ModelForm):
    class Meta:
        model = tbl_producto
        fields = ('mayorista', 'producto', 'categoria', 'cantidad', 'precio_unitario','precio_total',)
        labels = {
            'mayorista':'Proveedor',
            'producto':'Producto',
            'categoria':'Categorida',
            'cantidad':'Cantidad',
            'precio_unitario':'Precio por Unidad',
            'precio_total':'Precio total',
        }
        widgets = {
            'mayorista':forms.Select(attrs={'class':'form-control'}),
            'producto':forms.TextInput(attrs={'class':'form-control'}),
            'categoria':forms.Select(attrs={'class':'form-control'}),
            'cantidad':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_unitario':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_total':forms.NumberInput(attrs={'class':'form-control'}),
        }


