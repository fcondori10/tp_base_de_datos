from django.db import models

# Create your models here.
class Clientes(models.Model):
    dni = models.IntegerField( primary_key=True)
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.IntegerField()


class Pedidos(models.Model):
    id_pedido = models.AutoField( primary_key=True)
    id_producto= models.IntegerField()
    dni = models.IntegerField()
    cantidad = models.IntegerField()

class Productos(models.Model):
    id_producto = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)
