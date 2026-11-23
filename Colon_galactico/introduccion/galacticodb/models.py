from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField( max_length=50)




class CaraterísticasUsuarios():
    caracteristica = models.CharField(max_length=100)

    user= models.ForeignKey(Usuario,
        on_delete=models.PROTECT,
        related_name="usuarios")

class Nave():
    tamanio = models.CharField(max_length=100)
    capacidad = models.IntegerField(max_length=100)



class Misiones():
    descripcion = models.CharField(max_length=100)
    estado = models.BooleanField(default=False)

    nave= models.ForeignKey(Nave,
    on_delete=models.PROTECT,
    related_name="naves"
    )



class Exoplanetas():
    nombre = models.CharField(max_length=100)

