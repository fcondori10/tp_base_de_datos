"""
URL configuration for Tienda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestionTienda import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.gestion_tienda),
    path('agregar_cliente/', views.agregar_cliente),
    path('agregar_pedido/', views.agregar_pedido),
    path('agregar_producto/', views.agregar_producto),
    path('clientes_en_tablas/', views.clientes_en_tablas),
    path('pedidos_en_tablas/', views.pedidos_en_tablas),
    path('productos_en_tablas/', views.productos_en_tablas),


    path('modificar_cliente/', views.modificar_cliente),
    path('cliente_modificado/', views.cliente_modificado),
    path('modificar_pedido/', views.modificar_pedido),
    path('pedido_modificado/', views.pedido_modificado),
    path('modificar_producto/', views.modificar_producto),
    path('producto_modificado/', views.producto_modificado),
    path('eliminar_cliente/', views.eliminar_cliente),
    path('eliminar_pedido/', views.eliminar_pedido),
    path('eliminar_producto/', views.eliminar_producto),

    path('gestion_mongodb/', views.gestion_mongodb),
    path('agregar_producto_nosql/', views.agregar_producto_nosql),
    path('buscar_nosql/', views.buscar_nosql),
    path('eliminar_nosql/', views.eliminar_nosql),
    path('modificar_nosql/', views.modificar_nosql),








]
