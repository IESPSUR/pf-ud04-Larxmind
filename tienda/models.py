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


class Marca(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)
