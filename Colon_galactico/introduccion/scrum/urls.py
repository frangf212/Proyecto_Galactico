from django.contrib import admin
from django.urls import path

from galacticodb import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/usuarios/", views.devolverusuarios, name="usuarios"),
    path("api/usuario/<int:id>/", views.devolverusuarioid, name="usuario_id"),
    path("api/usuarios/crear/", views.crearusuario, name="crearusuario"),
    path("api/usuarios/<int:id>/actualizar/", views.actualizarusuario, name="actualizar_usuario"),
    path("api/usuarios/<int:id>/parcial/", views.actualizardato, name="actualizar_dato"),
    path("api/usuarios/<int:id>/eliminar/", views.borrarusuario, name="borrar_usuario"),
    path("api/misiones/asignar/", views.asignarmision, name="asignar_mision"),
    path("api/misiones/<int:id>/finalizar/", views.finalizarmision, name="finalizar_mision"),
    path("api/misiones/<int:id>/tripulantes/", views.listartripulantesenmision, name="tripulantes_mision"),

]