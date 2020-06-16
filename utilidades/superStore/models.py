from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# Create your models here.

class tbl_pais(models.Model):
    pais = models.CharField(max_length=50, help_text="Ingrese el pais de donde proviene")
    codigo_area = models.IntegerField(help_text="Ingrese el codigo de area")
    def __str__(self):
        return self.pais

    def get_absolute_url(self):
        return reverse('pais-detalle', args=[str(self.id)])

class tbl_departamento(models.Model):
    pais = models.ForeignKey(tbl_pais, on_delete=models.SET_NULL, null=True)
    departamento = models.CharField(max_length=50)

    def __str__(self):
        return self.departamento
    
    def get_absolute_url(self):
        return reverse('departamento-detalle', args=[str(self.id)])

class tbl_municipio(models.Model):
    departamento = models.ForeignKey(tbl_departamento, on_delete=models.SET_NULL, null=True)
    municipio = models.CharField(max_length=50)

    def __str__(self):
        return self.municipio
    def get_absolute_url(self):
        return reverse('municipio-detalle', args=[str(self.id)])

class tbl_barrio_canton(models.Model):
    municipio = models.ForeignKey(tbl_municipio, on_delete=models.SET_NULL, null=True)
    barrio_canton = models.CharField(max_length=50)

    def __str__(self):
        return self.barrio_canton
    def get_absolute_url(self):
        return reverse('barrio-detalle', args=[str(self.id)])


class tbl_tipo_usuario(models.Model):
    tipo_usuario = models.CharField(max_length=50, help_text="Ingrese el tipo de usuario")
    def __str__(self):
        return self.tipo_usuario

class User(AbstractUser):
    tipo_usuario_id = models.ForeignKey(tbl_tipo_usuario, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = "auth_user"

class tbl_cliente(models.Model):
    foto_perfil = models.ImageField(upload_to='photos_perfil_cliente', null=True)
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
    foto_perfil = models.ImageField(upload_to='photos_perfil_proveedor', null=True)
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
    barrio_canton = models.ForeignKey(tbl_barrio_canton ,on_delete=models.SET_NULL, null=True)
    direccion = models.TextField(max_length=200, help_text='Ingrese la direccion de la empresa', blank=True, null=True)

    def __str__(self):
        return "%s" % (self.nombre_empresa)

class tbl_categoria(models.Model):#modelo de categoria que almacenara todas las categorias existentes
    categoria = models.TextField(max_length=50)
    def __str__(self):
        return self.categoria

class tbl_producto(models.Model):#Tabla producto que almacenara todos los producto de todos los proveedores
    foto_producto1 = models.ImageField(upload_to='foto_producto', null=True)
    foto_producto2 = models.ImageField(upload_to='foto_producto', null=True)
    foto_producto3 = models.ImageField(upload_to='foto_producto', null=True)
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
    fecha_hora_realizada = models.DateTimeField(null=True, blank = True)
    cantidad = models.IntegerField(help_text="Ingrese la cantida vendida")
    precio_unitario = models.DecimalField(decimal_places=3, max_digits=10, help_text="Ingrese el precio unitario del producto")
    precio_total = models.DecimalField(decimal_places=3, max_digits=10, help_text="Ingrese el precio total de la venta")

    def __str__(self):
        return "producto %s " % self.producto_id

class tbl_cesta(models.Model):
    producto = models.ForeignKey(tbl_producto, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(tbl_cliente, on_delete=models.SET_NULL, null=True)
    fecha_hora_realizado = models.DateTimeField(blank=True, null=True)
    cantidad = models.IntegerField(help_text="Ingrese la cantidad de unidades")
    precio_unitario = models.DecimalField(decimal_places=3, max_digits=10, help_text="Ingrese el precio unitario de venta")
    precio_total = models.DecimalField(decimal_places=3, max_digits=10, help_text="Ingrese el precio total", blank=True, null=True)

    def __str__(self):
        return "%s, %s" % (self.producto, self.cliente)