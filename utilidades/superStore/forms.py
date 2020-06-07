from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, tbl_mayorista, tbl_cliente

class CreateUserForm(UserCreationForm):
   class Meta:
        model = User
        fields = ('username','email', 'first_name','last_name')
        labels={
            'username':'Nombre de Usuario',
            'email':'Correo',
            'first_name':'Nombres',
            'last_name':'Apellidos',
        }
class CreatePerfilCliente(forms.ModelForm):
    class Meta:
        model = tbl_cliente
        fields = ('user','genero','tipo_usuario_id','nombre_negocio','telefono','pais_id','fecha_nacimiento')
        labels = {
            'user':'Usuario',
            'genero':'Genero',
            'tipo_usuario_id':'Tipo de Usuario',
            'nombre_negocio':'Nombre del negocio',
            'telefono':'Telefono',
            'pais_id':'Pais',
            'fecha_nacimiento':'Fecha de nacimiento',
        }
        widgets={
            'user':forms.Select(attrs={'class':'form-control'}),
            'genero':forms.Select(attrs={'class':'form-control'}),
            'tipo_usuario_id':forms.Select(attrs={'class':'form-control'}),
            'nombre_negocio':forms.TextInput(attrs={'class':'form-control'}),
            'telefono':forms.TextInput(attrs={'class':'form-control'}),
            'pais_id':forms.Select(attrs={'class':'form-control'}),
            'fecha_nacimiento':forms.TextInput(attrs={'class':'form-control'}),
        }
    

