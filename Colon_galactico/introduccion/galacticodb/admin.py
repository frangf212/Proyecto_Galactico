from django.contrib import admin
from .models import Usuario
from .models import Nave
from .models import CaraterísticasUsuarios
from .models import Exoplanetas
from .models import Misiones


# Register your models here.
admin.site.register(Usuario)
admin.site.register(Nave)
admin.site.register(CaraterísticasUsuarios)
admin.site.register(Exoplanetas)
admin.site.register(Misiones)