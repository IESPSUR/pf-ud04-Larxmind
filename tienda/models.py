from django.conf import settings
from django.db import models

# Create your models here.


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    unidades = models.IntegerField()
    precio = models.FloatField()
    detalles = models.TextField()
    marca = models.ForeignKey('Marca', on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)
    def __str__(self):
        return self.nombre


class Compra(models.Model):
    nombre = models.ForeignKey('Producto', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=True)
    unidades = models.IntegerField(default=1)
    importe = models.FloatField()


