from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class tbl_pais(models.Model):
    pais = models.CharField(max_length=50, help_text="Ingrese el pais de donde proviene")
    codigo_area = models.IntegerField(help_text="Ingrese el codigo de area")
    def __str__(self):
        return self.pais

class tbl_tipo_usuario(models.Model):
    tipo_usuario = models.CharField(max_length=50, help_text="Ingrese el tipo de usuario")
    def __str__(self):
        return self.tipo_usuario

class User(AbstractUser):
    tipo_usuario_id = models.ForeignKey(tbl_tipo_usuario, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = "auth_user"

class tbl_cliente(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    GEN = (
        ('M','Masculino'),
        ('F','Femenino'),
    )
    genero = models.CharField(max_length=1, choices=GEN, blank=True, default='M',help_text='Ingrese su genero')
    nombre_negocio = models.CharField(max_length=50, help_text="Ingrese el nombre de su negocio")
    telefono = models.CharField(max_length=8, help_text="Ingrese su numero de telefono")
    pais_id = models.ForeignKey(tbl_pais, on_delete=models.SET_NULL, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return "%s" % (self.nombre_negocio)

class tbl_mayorista(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    GEN = (
        ('M','Masculino'),
        ('F','Femenino'),
    )
    genero = models.CharField(max_length=1, choices=GEN, blank=True, default='M',help_text='Ingrese su genero')
    nombre_empresa = models.CharField(max_length=50, help_text="Ingrese el nombre de su empresa")
    telefono = models.CharField(max_length=8, help_text="Ingrese su numero de telefono")
    pais_id = models.ForeignKey(tbl_pais, on_delete=models.SET_NULL, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return "%s" % (self.nombre_empresa)