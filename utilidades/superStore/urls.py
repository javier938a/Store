from django.urls import path
from .views import index, register, RegistrarPerfilCliente, logiar

app_name='tienda'
urlpatterns=[
    path('', index.as_view(), name='index'),
    path('registrar', register, name='registrar'),
    path('registrar/perfil/<str:username>', RegistrarPerfilCliente, name='perfil'),
    path('login', logiar, name='login')
]