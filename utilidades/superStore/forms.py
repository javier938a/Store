from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, tbl_mayorista, tbl_cliente, tbl_direccion, tbl_producto, tbl_venta
from .models import tbl_cesta
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
        fields = ('foto_perfil','user','genero','nombre_negocio','telefono','pais_id','fecha_nacimiento')
        labels = {
            'foto_perfil':'Foto de Perfil',
            'user':'Usuario',
            'genero':'Genero',
            'nombre_negocio':'Nombre del negocio',
            'telefono':'Telefono',
            'pais_id':'Pais',
            'fecha_nacimiento':'Fecha de nacimiento',
        }
        widgets={
            'foto_perfil':forms.FileInput(attrs={'class':'form-control', 'id':'foto'}),
            'user':forms.Select(attrs={'class':'form-control'}),
            'genero':forms.Select(attrs={'class':'form-control'}),
            'nombre_negocio':forms.TextInput(attrs={'class':'form-control'}),
            'telefono':forms.TextInput(attrs={'class':'form-control'}),
            'pais_id':forms.Select(attrs={'class':'form-control'}),
            'fecha_nacimiento':forms.DateInput(attrs={'class':'form-control vDateField'}),
        }

class CreatePerfilMayorista(forms.ModelForm):#Registra el perfil del proveedor
    class Meta:
        model = tbl_mayorista
        fields = ('foto_perfil','user','genero','nombre_empresa','telefono','pais_id','fecha_nacimiento','direccion')
        labels = {
            'foto_perfil':'Foto de Perfil',
            'user':'Usuario',
            'genero':'Genero',
            'nombre_empresa':'Empresa',
            'telefono':'Telefono',
            'pais_id':'Pais',
            'fecha_nacimiento':'Fecha de nacimiento',
            'direccion':'Direccion de la empresa',
        }
        widgets={
            'foto_perfil':forms.FileInput(attrs={'class':'form-control'}),
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

class FormCrearVenta(forms.ModelForm):
    class Meta:
        model = tbl_venta
        fields = ('cliente_id', 'producto_id','cantidad', 'precio_unitario', 'precio_total',)
        labels = {
            'cliente_id':'Cliente',
            'producto_id':'Producto',
            'cantidad':'Cantidad',
            'precio_unitario':'Precio Unitario',
            'precio_total':'Precio Total',
        }
        widgets = {
            'cliente_id':forms.Select(attrs={'class':'form-control'}),
            'producto_id':forms.Select(attrs={'class':'form-control'}),
            'cantidad':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_unitario':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_total':forms.NumberInput(attrs={'class':'form-control'}),
        }

class FormCrearCesta(forms.ModelForm):
    class Meta:
        model = tbl_cesta
        fields = ('producto', 'cliente', 'fecha_hora_realizado', 'cantidad', 'precio_unitario', 'precio_total')
        labels = {
            'producto':'Producto',
            'cliente':'Cliente',
            'fecha_hora_realizado':'Fecha de transaccion',
            'cantidad':'Cantidad',
            'precio_unitario':'Precio Unitario',
            'precio_total':'Precio Total',
        }
        widgets = {
            'producto':forms.Select(attrs={'class':'form-control'}),
            'cliente':forms.Select(attrs={'class':'form-control'}),
            'fecha_hora_realizado':forms.DateTimeInput(attrs={'class':'form-control'}),
            'cantidad':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_unitario':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_total':forms.NumberInput(attrs={'class':'form-control'}),
        }
        



