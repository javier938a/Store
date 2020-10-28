from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
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

class UserManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractUser):
    tipo_usuario_id = models.ForeignKey(tbl_tipo_usuario, on_delete=models.SET_NULL, null=True)
    objects=UserManager()
    #email = models.EmailField('email address', unique=True)
    #USERNAME_FIELD='email'
    #REQUIRED_FIELDS=['username']
    
    class Meta:
        db_table = "auth_user"
        unique_together = [['username' ,'first_name', 'last_name']]
    
    def natural_key(self):
        return (self.username, self.first_name, self.last_name)

class tbl_cliente(models.Model):
    foto_perfil = models.ImageField(verbose_name="Imagen", max_length=300, upload_to="fotoPerfilCliente", blank=True, null=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE, blank=True, null=True)
    GEN = (
        ('M','Masculino'),
        ('F','Femenino'),
    )
    genero = models.CharField(max_length=1, choices=GEN, blank=True, default='M',help_text='Ingrese su genero')
    telefono = models.CharField(max_length=8, help_text="Ingrese su numero de telefono")
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return "%s" % self.user 

class tbl_direccion(models.Model):
    cliente = models.ForeignKey(tbl_cliente, on_delete=models.SET_NULL, null=True)
    pais = models.TextField(max_length=200, help_text="Ingrese el departamento", null=True)
    departamento = models.TextField(max_length=200, help_text="Ingrese el departamento", null=True)
    municipio = models.TextField(max_length=200, help_text="Ingrese el departamento", null=True)
    barrio_canton = models.TextField(max_length=200, help_text="Ingrese el departamento", null=True)
    calle = models.TextField(max_length=400, help_text="Ingrese el departamento", null=True)
    referencia = models.TextField(max_length=200, help_text="Ingrese el departamento", null=True)
    estado = models.BooleanField(null=True, blank=True, help_text="seleccione si esta activo o no esta direccion")
    def __str__(self):
        return "%s %s %s %s %s %s %s" % (self.cliente, self.pais, self.departamento, self.municipio, self.barrio_canton, self.calle, self.referencia)


class tbl_mayorista(models.Model):
    foto_perfil = models.ImageField(verbose_name='Imagen', max_length=300 , upload_to='foto_perfil_proveedor', null=True, blank=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    objetivo = models.TextField(max_length=300, help_text="Ingrese informacion de su empresa al sector a que se dedica y su objetivo", null=True)
    GEN = (
        ('M','Masculino'),
        ('F','Femenino'),
    )
    genero = models.CharField(max_length=1, choices=GEN, blank=True, default='M',help_text='Ingrese su genero')
    nombre_empresa = models.CharField(max_length=50, help_text="Ingrese el nombre de su empresa")
    telefono = models.CharField(max_length=8, help_text="Ingrese su numero de telefono")
    fecha_nacimiento = models.DateField(null=True, blank=True)
    barrio_canton = models.ForeignKey(tbl_barrio_canton, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return "%s" % (self.nombre_empresa)

class tbl_seguidores(models.Model):
    mayorista = models.ForeignKey(tbl_mayorista, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(tbl_cliente, on_delete=models.SET_NULL, null=True)
    fecha_de_seguidor = models.DateTimeField(null=True)
    grupo_privado = models.CharField(max_length=50, help_text="Escriba nombre grupo privado", null=True)
    

    def __str__(self):
        return "%s %s"%(self.mayorista, self.cliente)

class tbl_categoria(models.Model):#modelo de categoria que almacenara todas las categorias existentes
    categoria = models.TextField(max_length=50)
    icono = models.ImageField(verbose_name="Imagen", upload_to="iconos_cate", null=True)
    def __str__(self):
        return self.categoria
class tbl_sub_categoria1(models.Model):
    categoria = models.ForeignKey(tbl_categoria, on_delete=models.SET_NULL, null=True)
    sub_categoria = models.CharField(max_length=50, help_text="Ingrese la subcategoria")
    def __str__(self):
        return self.sub_categoria
    
    def get_absolute_url(self):
        return reverse("categoria-detalle",args=[str(self.id)])

class tbl_producto(models.Model):#Tabla producto que almacenara todos los producto de todos los proveedores
    codigo_producto = models.CharField(max_length=50, help_text="Ingrese el codigo del producto", null=True)
    foto_producto1 = models.ImageField(verbose_name="Imagen", upload_to='foto_producto', null=True, blank=True)
    foto_producto2 = models.ImageField(verbose_name="Imagen", upload_to='foto_producto', null=True, blank=True)
    foto_producto3 = models.ImageField(verbose_name="Imagen", upload_to='foto_producto', null=True, blank=True)
    url = models.SlugField(max_length=150, null=True, blank=True)
    mayorista = models.ForeignKey(tbl_mayorista, on_delete=models.CASCADE, blank=True)
    producto = models.CharField(max_length=100, help_text="Ingrese el nombre el producto")
    info_producto = models.TextField(max_length=1000, null=True)
    fecha_registro = models.DateField(null=True, blank=True)
    costo_envio = models.FloatField(help_text="Costo del envio", null=True)
    medio_de_envio = models.CharField(max_length=100, help_text="empresa por donde se envia el producto", null=True)
    cantidad = models.IntegerField(help_text="Ingrese la cantidad del producto")
    precio_unitario = models.FloatField(help_text="Ingrese el precio unitario de compra del producto")
    precio_venta = models.FloatField(help_text="Ingrese el precio unitario de venta del producto", null=True)
    precio_total = models.FloatField(help_text="precio total en inventario", blank=True, null=True)
    precio_total_venta=models.FloatField(help_text="Ingrese el precio total de venta", null=True)
    sub_categoria1 = models.ForeignKey(tbl_sub_categoria1, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.producto
    
    def get_absolute_url(self):
        return reverse('producto', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        self.url = slugify(self.producto)
        super(tbl_producto, self).save(*args, **kwargs)

class tbl_estado_envio(models.Model):#Se define al tabla estado del envio 
    estado = models.CharField(max_length=115)
    def __str__(self):
        return self.estado

class tbl_factura(models.Model):
    numero_factura=models.CharField(help_text="Numero de factura", max_length=50, null=True, blank=True)
    cliente = models.CharField(max_length=50, help_text='Nombre del cliente', null=True, blank=True)
    direccion=models.TextField(max_length=100, help_text='Direccion del cliente', null=True, blank=True)
    Fecha_hora=models.DateTimeField(help_text='Fecha en que se genera la factura', null=True, blank=True)
    nit=models.CharField(help_text='Nit de la empresa', max_length=17, null=True, blank=True)
    
    def __str__(self):
        return "factura N° %s cliente %s "%(self.numero_factura, self.cliente)
    


class tbl_venta(models.Model):#almacenara las ventas efectuadas por los mayoristas por parte de los clientes
    cliente_id = models.ForeignKey(tbl_cliente, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(tbl_producto, on_delete=models.CASCADE)
    fecha_hora_realizada = models.DateTimeField(null=True, blank = True)
    cantidad = models.IntegerField(help_text="Ingrese la cantida vendida")
    precio_unitario = models.DecimalField(decimal_places=3, max_digits=10, help_text="Ingrese el precio unitario del producto")
    precio_total = models.DecimalField(decimal_places=3, max_digits=10, help_text="Ingrese el precio total de la venta", null=True, blank=True)
    direccion = models.ForeignKey(tbl_direccion, on_delete=models.SET_NULL, null=True, blank=True)
    estado_envio = models.ForeignKey(tbl_estado_envio, on_delete=models.SET_NULL, null=True, blank=True)
    factura = models.ForeignKey(tbl_factura, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return "producto %s " % self.producto_id

class tbl_comentario_producto(models.Model):
    cliente = models.ForeignKey(tbl_cliente, on_delete=models.SET_NULL, null=True)
    producto = models.ForeignKey(tbl_producto, on_delete=models.SET_NULL, null=True)
    comentario = models.TextField(max_length=500, help_text="Ingrese un comentario sobre su experiencia de compra")
    puntaje = models.IntegerField(help_text="Ingrese un puntaja evaluando al vendedor de esta manera ayuda a que otras personas tengan mas confianza para comprar en la tienda")
    foto_prueba1=models.ImageField(verbose_name="Image", upload_to="foto_prueba", null=True, blank=True)
    foto_prueba2=models.ImageField(verbose_name="Image", upload_to='foto_prueba', null=True, blank=True)
    foto_prueba3=models.ImageField(verbose_name="Image", upload_to='foto_prueba', null=True, blank=True)
    fecha_creacion=models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return " %s: %s" % (self.cliente, self.comentario)

class tbl_cesta(models.Model):
    producto = models.ForeignKey(tbl_producto, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(tbl_cliente, on_delete=models.SET_NULL, null=True)
    fecha_hora_realizado = models.DateTimeField(blank=True, null=True)
    cantidad = models.IntegerField(help_text="Ingrese la cantidad de unidades")
    precio_unitario = models.DecimalField(decimal_places=3, max_digits=10, help_text="Ingrese el precio unitario de venta")
    precio_total = models.DecimalField(decimal_places=3, max_digits=10, help_text="Ingrese el precio total", blank=True, null=True)
    direccion = models.ForeignKey(tbl_direccion, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return "%s, %s" % (self.producto, self.cliente)

class tbl_favoritos(models.Model):
    cliente = models.ForeignKey(tbl_cliente, on_delete=models.SET_NULL, null=True)
    producto = models.ForeignKey(tbl_producto, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return "%s" % (self.producto.producto)    

class tbl_clients_connect(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    canal = models.TextField(help_text="Ingrese el canal unico", max_length=10000)
    estado = models.BooleanField(help_text="seleccione para saber si esta conectado", null=True)
    fecha_connect = models.DateTimeField(help_text="fecha y hora de conecccion", null=True, blank=True)
    fecha_disconnect= models.DateTimeField(help_text="fecha y hora de desconeccion", null=True, blank=True)
    def __str__(self):
        return "%s --> %s" % (str(self.usuario), str(self.canal))

class tbl_bandeja_de_salida_cliente(models.Model):
    mayorista=models.ForeignKey(tbl_mayorista, on_delete=models.SET_NULL, null=True)
    cliente=models.ForeignKey(tbl_cliente, on_delete=models.SET_NULL, null=True)
    mensaje=models.TextField(max_length=1000)
    fecha=models.DateTimeField(null=True)
    grupo=models.CharField(max_length=40)

    def __str__(self):
        return "%s --> %s" %(str(self.cliente),self.mensaje)

class tbl_bandeja_de_entrada_cliente(models.Model):
    mayorista=models.ForeignKey(tbl_mayorista, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(tbl_cliente, on_delete=models.SET_NULL, null=True)
    mensaje_salida=models.ForeignKey(tbl_bandeja_de_salida_cliente, on_delete=models.SET_NULL, null=True)
    mensaje=models.TextField(max_length=1000)
    fecha=models.DateTimeField(null=True)
    grupo=models.CharField(max_length=40)
    
    def __str__(self):
        return "%s --> %s" % (str(self.mayorista), self.mensaje)

class tbl_bandeja_de_salida_mayorista(models.Model):
    cliente=models.ForeignKey(tbl_cliente, on_delete=models.SET_NULL, null=True)
    mayorista=models.ForeignKey(tbl_mayorista, on_delete=models.SET_NULL, null=True)
    mensaje=models.TextField(max_length=1000)
    fecha=models.DateTimeField(null=True)
    grupo=models.CharField(max_length=40)

    def __str__(self):
        return "%s --> %s" % (str(self.mayorista), self.mensaje)

class tbl_bandeja_de_entrada_mayorista(models.Model):
    cliente=models.ForeignKey(tbl_cliente, on_delete=models.SET_NULL, null=True)
    mayorista=models.ForeignKey(tbl_mayorista, on_delete=models.SET_NULL, null=True)
    mensaje_salida=models.ForeignKey(tbl_bandeja_de_salida_mayorista, on_delete=models.SET_NULL, null=True, blank=True)
    mensaje=models.TextField(max_length=1000)
    fecha=models.DateTimeField(null=True)
    grupo=models.CharField(max_length=40)

    def __str__(self):
        return "%s --> %s" %(str(self.cliente), self.mensaje)



    


 
