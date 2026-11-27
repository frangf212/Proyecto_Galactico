import json
from json import JSONDecodeError

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Participacion, Usuario, Mision


def devolverusuarios(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Operación no permitida"},
            status=405
        )

    usuarios = Usuario.objects.values()
    return JsonResponse(list(usuarios), safe=False)


def devolverusuarioid(request, id):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Operación no permitida"},
            status=405
        )

    usuario = Usuario.objects.filter(id=id).values().first()

    if usuario is None:
        return JsonResponse(
            {"error": "Usuario no encontrado"},
            status=404
        )

    return JsonResponse(usuario)


@csrf_exempt
def crearusuario(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Operación no permitida"},
            status=405
        )

    try:
        datos = json.loads(request.body)
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "JSON inválido"},
            status=400
        )

    if not isinstance(datos, dict):
        return JsonResponse(
            {"error": "Se esperaba un objeto JSON"},
            status=400
        )

    nombre = datos.get("nombre")
    if not isinstance(nombre, str) or not nombre.strip():
        return JsonResponse(
            {"error": "El nombre es obligatorio"},
            status=400
        )

    nuevo_usuario = Usuario.objects.create(nombre=nombre.strip())

    return JsonResponse(
        {
            "mensaje": "Usuario creado correctamente",
            "id": nuevo_usuario.id
        },
        status=201
    )


@csrf_exempt
def actualizarusuario(request, id):
    if request.method != "PUT":
        return JsonResponse(
            {"error": "Operación no permitida"},
            status=405
        )

    try:
        datos = json.loads(request.body)
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "JSON inválido"},
            status=400
        )

    if not isinstance(datos, dict):
        return JsonResponse(
            {"error": "Se esperaba un objeto JSON"},
            status=400
        )

    usuario = Usuario.objects.filter(id=id).first()
    if usuario is None:
        return JsonResponse(
            {"error": "Usuario no encontrado"},
            status=404
        )

    nombre = datos.get("nombre")
    if not isinstance(nombre, str) or not nombre.strip():
        return JsonResponse(
            {"error": "El nombre es obligatorio"},
            status=400
        )

    usuario.nombre = nombre.strip()
    usuario.save()

    return JsonResponse({
        "mensaje": "Usuario actualizado correctamente",
        "id": usuario.id
    })


@csrf_exempt
def actualizardato(request, id):
    if request.method != "PATCH":
        return JsonResponse(
            {"error": "Operación no permitida"},
            status=405
        )

    try:
        datos = json.loads(request.body)
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "JSON inválido"},
            status=400
        )

    if not isinstance(datos, dict):
        return JsonResponse(
            {"error": "Se esperaba un objeto JSON"},
            status=400
        )

    usuario = Usuario.objects.filter(id=id).first()
    if usuario is None:
        return JsonResponse(
            {"error": "Usuario no encontrado"},
            status=404
        )

    if "nombre" in datos:
        nombre = datos["nombre"]
        if not isinstance(nombre, str) or not nombre.strip():
            return JsonResponse(
                {"error": "El nombre debe ser un texto no vacío"},
                status=400
            )
        usuario.nombre = nombre.strip()

    usuario.save()

    return JsonResponse({
        "mensaje": "Usuario actualizado correctamente",
        "id": usuario.id,
        "nombre": usuario.nombre
    })


@csrf_exempt
def borrarusuario(request, id):
    if request.method != "DELETE":
        return JsonResponse(
            {"error": "Operación no permitida"},
            status=405
        )

    usuario = Usuario.objects.filter(id=id).first()
    if usuario is None:
        return JsonResponse(
            {"error": "Usuario no encontrado"},
            status=404
        )

    if Participacion.objects.filter(usuario=usuario).exists():
        return JsonResponse(
            {"error": "No se puede eliminar un usuario que ha participado en misiones"},
            status=400
        )

    usuario.delete()
    return HttpResponse(status=204)

def listartripulantesenmision(request, id):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Operación no permitida"},
            status=405
        )

    mision = Mision.objects.filter(id=id).first()
    if mision is None:
        return JsonResponse(
            {"error": "Misión no encontrada"},
            status=404
        )

    tripulacion = []
    for participacion in Participacion.objects.filter(mision=mision).order_by("rol"):
        tripulacion.append({
            "usuario_id": participacion.usuario.id,
            "nombre": participacion.usuario.nombre,
            "rol": participacion.rol
        })

    return JsonResponse({
        "mision_id": mision.id,
        "descripcion": mision.descripcion,
        "estado": mision.estado,
        "nave": mision.nave.tamanio,
        "tripulacion": tripulacion
    })