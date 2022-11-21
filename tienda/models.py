from django.conf import settings
from django.db import models
from django import forms


# Create your models here.


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    unidades_disponibles = models.IntegerField()
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
    producto = models.ForeignKey('Producto', on_delete=models.RESTRICT)
    fecha = models.DateTimeField(auto_now=True)
    unidades_solicitadas = models.IntegerField(default=1)
    importe = models.FloatField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)


class CheckOutForm(forms.Form):
    cantidad_requerida = forms.IntegerField(label='cantidad_requerida')




