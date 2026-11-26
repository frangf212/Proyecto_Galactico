from django.contrib import admin
from .models import (
    CaracteristicaUsuario,
    Exoplaneta,
    Mision,
    Nave,
    Participacion,
    Usuario,
)

admin.site.register(Usuario)
admin.site.register(CaracteristicaUsuario)
admin.site.register(Nave)
admin.site.register(Mision)
admin.site.register(Participacion)
admin.site.register(Exoplaneta)

