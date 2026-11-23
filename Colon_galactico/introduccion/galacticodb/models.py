from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField( max_length=50)

    def __str__(self):
        return self.nombre




class CaraterísticasUsuarios(models.Model):
    caracteristica = models.CharField(max_length=100)

    user= models.ForeignKey(Usuario,
        on_delete=models.PROTECT,
        related_name="usuarios")
    def __str__(self):
        return self.user.nombre

class Nave(models.Model):
    tamanio = models.CharField(max_length=100)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.tamanio



class Misiones(models.Model):
    descripcion = models.CharField(max_length=100)
    estado = models.BooleanField(default=False)

    nave= models.ForeignKey(Nave,
    on_delete=models.PROTECT,
    related_name="naves"
    )

    def __str__(self):
        return self.nave.tamanio



class Exoplanetas(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
