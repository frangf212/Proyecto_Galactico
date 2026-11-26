from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class CaracteristicaUsuario(models.Model):
    caracteristica = models.CharField(max_length=100)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="caracteristicas"
    )

    def __str__(self):
        return f"{self.usuario} - {self.caracteristica}"


class Nave(models.Model):
    tamanio = models.CharField(max_length=20)
    capacidad = models.IntegerField()  # solo tripulantes

    def __str__(self):
        return f"{self.tamanio} #{self.pk}"


class Mision(models.Model):
    descripcion = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, default="en_curso")  # en_curso, exito, fracaso
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    nave = models.ForeignKey(Nave, on_delete=models.PROTECT, related_name="misiones")

    def __str__(self):
        return f"{self.descripcion} ({self.estado})"


class Participacion(models.Model):
    rol = models.CharField(max_length=20)  # capitan, tripulante
    mision = models.ForeignKey(
        Mision, on_delete=models.CASCADE, related_name="participaciones"
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, related_name="participaciones"
    )

    def __str__(self):
        return f"{self.usuario} - {self.rol} - {self.mision}"


class Exoplaneta(models.Model):
    nombre = models.CharField(max_length=100)
    mision = models.ForeignKey(
        Mision, on_delete=models.CASCADE, related_name="exoplanetas"
    )

    def __str__(self):
        return self.nombre