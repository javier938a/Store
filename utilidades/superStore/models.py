from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
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

class tbl_direccion(models.Model):
    cliente = models.ForeignKey(tbl_cliente, on_delete=models.SET_NULL, null=True)
    direccion = models.TextField(max_length=200, help_text="ingresa la direccion del cliente")
    estado = models.BooleanField(null=True, blank=True, help_text="seleccione si esta activo o no esta direccion")
    def __str__(self):
        return self.direccion


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
    direccion = models.TextField(max_length=200, help_text='Ingrese la direccion de la empresa', blank=True, null=True)

    def __str__(self):
        return "%s" % (self.nombre_empresa)

class tbl_categoria(models.Model):#modelo de categoria que almacenara todas las categorias existentes
    categoria = models.TextField(max_length=50)
    def __str__(self):
        return self.categoria

class tbl_producto(models.Model):#Tabla producto que almacenara todos los producto de todos los proveedores
    mayorista = models.ForeignKey(tbl_mayorista, on_delete=models.CASCADE, blank=True)
    producto = models.CharField(max_length=100, help_text="Ingrese el nombre el producto")
    categoria = models.ForeignKey(tbl_categoria, on_delete=models.CASCADE)
    cantidad = models.IntegerField(help_text="Ingrese la cantidad del producto")
    precio_unitario = models.FloatField(help_text="Ingrese el precio unitario del producto")
    precio_total = models.FloatField(help_text="precio total en inventario")

    def __str__(self):
        return self.producto

    def get_absolute_url(self):
        return reverse('producto', args=[str(self.id)])

class tbl_venta(models.Model):#almacenara las ventas efectuadas por los mayoristas por parte de los clientes
    cliente_id = models.ForeignKey(tbl_cliente, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(tbl_producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(help_text="Ingrese la cantida vendida")
    precio_unitario = models.FloatField(help_text="Ingrese el precio unitario del producto")
    precio_total = models.FloatField(help_text="Ingrese el precio total de la venta")

    def __str__(self):
        return "producto %d " % self.producto_id

