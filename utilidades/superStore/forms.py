from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, tbl_mayorista, tbl_cliente, tbl_direccion, tbl_producto, tbl_venta, tbl_categoria, tbl_pais
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
        fields = ('foto_perfil','user','genero','telefono','fecha_nacimiento')
        labels = {
            'foto_perfil':'Foto de Perfil',
            'user':'Usuario',
            'genero':'Genero',
            'telefono':'Telefono',
            'fecha_nacimiento':'Fecha de nacimiento',
        }
        widgets={
            'foto_perfil':forms.FileInput(attrs={'class':'form-control', 'id':'foto'}),
            'user':forms.Select(attrs={'class':'form-control'}),
            'genero':forms.Select(attrs={'class':'form-control'}),
            'telefono':forms.TextInput(attrs={'class':'form-control'}),
            'fecha_nacimiento':forms.DateInput(attrs={'class':'form-control vDateField'}),
        }

class CreatePerfilMayorista(forms.ModelForm):#Registra el perfil del proveedor
    class Meta:
        model = tbl_mayorista
        fields = ('foto_perfil','user','objetivo','genero','nombre_empresa','telefono','fecha_nacimiento','barrio_canton',)
        labels = {
            'foto_perfil':'Foto de Perfil',
            'user':'Usuario',
            'objetivo':'Acerca de la Empresa',
            'genero':'Genero',
            'nombre_empresa':'Empresa',
            'telefono':'Telefono',
            'fecha_nacimiento':'Fecha de nacimiento',
            'barrio_canton':'Barrio o Canton'

        }
        widgets={
            'foto_perfil':forms.FileInput(attrs={'class':'form-control', 'id':'foto'}),
            'user':forms.Select(attrs={'class':'form-control'}),
            'objetivo':forms.Textarea(attrs={'class':'form-control'}),
            'genero':forms.Select(attrs={'class':'form-control'}),
            'nombre_empresa':forms.TextInput(attrs={'class':'form-control'}),
            'telefono':forms.TextInput(attrs={'class':'form-control'}),
            'fecha_nacimiento':forms.DateInput(attrs={'class':'form-control vDateField'}),
            'barrio_canton':forms.Select(attrs={'class':'form-control'}),
        } 
class FormDireP(forms.Form):
    pais = forms.ModelMultipleChoiceField(queryset=None,required=False, label="Pais", widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    depto = forms.ChoiceField(label="Departamento",required=False, widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    muni = forms.ChoiceField(label="Municipio",required=False, widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pais'].queryset = tbl_pais.objects.all()


class FormCrearDireccion(forms.ModelForm):#para registrar las multiples direcciones que pueda tener un cliente
    class Meta:
        model = tbl_direccion
        fields = ('cliente','pais','departamento','municipio','barrio_canton','calle','referencia','estado')  
        labels = {
            'cliente':'Cliente',
            'pais':'Pais',
            'departamento':'Departamento',
            'municipio':'Municipio',
            'barrio_canton':'Barrio o Canton',
            'calle':'Calle',
            'referencia':'Referencia',
            'estado':'¿Asignar como su direccion actual?',
        }
        widgets= {
            'cliente':forms.Select(attrs={'class':'form-control'}),
            'pais':forms.TextInput(attrs={'class':'form-control'}),
            'departamento':forms.TextInput(attrs={'class':'form-control'}),
            'municipio':forms.TextInput(attrs={'class':'form-control'}),
            'barrio_canton':forms.TextInput(attrs={'class':'form-control'}),
            'calle':forms.TextInput(attrs={'class':'form-control'}),
            'referencia':forms.TextInput(attrs={'class':'form-control'}),
            'estado':forms.CheckboxInput(attrs={'class':'form-control'}),
        }

class FormCrearProducto(forms.ModelForm):
    class Meta:
        model = tbl_producto
        fields = ('codigo_producto','foto_producto1','foto_producto2','foto_producto3','mayorista', 'producto','info_producto','medio_de_envio', 'cantidad', 'precio_unitario','precio_venta','costo_envio','sub_categoria1')
        labels = {
            'codigo_producto':'Codigo de Producto',
            'foto_producto1':'Foto del producto No1',
            'foto_producto2':'Foto del producto No2',
            'foto_producto3':'Foto del producto No3',
            'mayorista':'Proveedor',
            'producto':'Producto',
            'info_producto':'Descripcion',
            'medio_de_envio':'Medio de envio',
            'cantidad':'Cantidad',
            'precio_unitario':'Precio de compra por Unidad',
            'precio_venta':'Precio de venta por Unidad',
            'costo_envio':'Costo de envio',
            'sub_categoria1':'Categoria',
        }
        widgets = {
            'codigo_producto':forms.TextInput(attrs={'class':'form-control'}),
            'foto_producto1':forms.FileInput(attrs={'class':'form-control'}),
            'foto_producto2':forms.FileInput(attrs={'class':'form-control'}),
            'foto_producto3':forms.FileInput(attrs={'class':'form-control'}),
            'mayorista':forms.Select(attrs={'class':'form-control'}),
            'producto':forms.TextInput(attrs={'class':'form-control'}),
            'info_producto':forms.TextInput(attrs={'class':'form-control'}),   
            'medio_de_envio':forms.TextInput(attrs={'class':'form-control'}),
            'cantidad':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_unitario':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_venta':forms.NumberInput(attrs={'class':'form-control'}),
            'costo_envio':forms.NumberInput(attrs={'class':'form-control'}),
            'sub_categoria1':forms.Select(attrs={'class':'form-control'})
        }

class SubCateForm(forms.Form):
    categoria1 = forms.ChoiceField(label="Categoria nivel 1", widget=forms.Select(attrs={'required':False}))
        

class FormCrearVenta(forms.ModelForm):
    class Meta:
        model = tbl_venta
        fields = ('cliente_id', 'producto_id','cantidad', 'precio_unitario','direccion',)
        labels = {
            'cliente_id':'Cliente',
            'producto_id':'Producto',
            'cantidad':'Cantidad',
            'precio_unitario':'Precio Unitario',
            'direccion':'Direccion',
        }
        widgets = {
            'cliente_id':forms.Select(attrs={'class':'form-control'}),
            'producto_id':forms.Select(attrs={'class':'form-control'}),
            'cantidad':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_unitario':forms.NumberInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'direccion':forms.Select(attrs={'class':'form-control'}),
        }

class FormCrearCesta(forms.ModelForm):
    class Meta:
        model = tbl_cesta
        fields = ('producto', 'cliente', 'cantidad', 'precio_unitario', 'direccion',)
        labels = {
            'producto':'Producto',
            'cliente':'Cliente',
            'cantidad':'Cantidad',
            'precio_unitario':'Precio Unitario',
            'precio_total':'Precio Total',
            'direccion':'Direccion',
        }
        widgets = {
            'producto':forms.Select(attrs={'class':'form-control', }),
            'cliente':forms.Select(attrs={'class':'form-control'}),
            'cantidad':forms.NumberInput(attrs={'class':'form-control'}),
            'precio_unitario':forms.NumberInput(attrs={'class':'form-control','readonly':'readonly'}),
            'direccion':forms.Select(attrs={'class':'form-control'}),
        }
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = tbl_categoria
        fields=('categoria',)
