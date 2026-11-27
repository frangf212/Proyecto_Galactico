import json
from json import JSONDecodeError

from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Exoplaneta, Mision, Nave, Participacion, Usuario
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



@csrf_exempt
def asignarmision(request):
    if request.method != "POST":
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

    descripcion = datos.get("descripcion")
    if not isinstance(descripcion, str) or not descripcion.strip():
        return JsonResponse(
            {"error": "La descripción es obligatoria"},
            status=400
        )

    nave_id = datos.get("nave_id")
    if not isinstance(nave_id, int):
        return JsonResponse(
            {"error": "El campo nave_id es obligatorio y debe ser un entero"},
            status=400
        )

    nave = Nave.objects.filter(id=nave_id).first()
    if nave is None:
        return JsonResponse(
            {"error": "La nave no existe"},
            status=404
        )

    capitanes = datos.get("capitanes", [])
    tripulantes = datos.get("tripulantes", [])

    if not isinstance(capitanes, list) or not all(isinstance(i, int) for i in capitanes):
        return JsonResponse(
            {"error": "capitanes debe ser una lista de IDs enteros"},
            status=400
        )
    if not isinstance(tripulantes, list) or not all(isinstance(i, int) for i in tripulantes):
        return JsonResponse(
            {"error": "tripulantes debe ser una lista de IDs enteros"},
            status=400
        )

    if len(capitanes) != len(set(capitanes)) or len(tripulantes) != len(set(tripulantes)):
        return JsonResponse(
            {"error": "No se permiten usuarios repetidos en capitanes o tripulantes"},
            status=400
        )
    if set(capitanes).intersection(set(tripulantes)):
        return JsonResponse(
            {"error": "Un mismo usuario no puede ser capitán y tripulante a la vez"},
            status=400
        )

    tamanio = (nave.tamanio or "").strip().lower()
    if tamanio in ["pequena", "pequeña", "mediana"] and len(capitanes) != 1:
        return JsonResponse(
            {"error": "Las naves pequeñas y medianas deben tener exactamente un capitán"},
            status=400
        )
    if tamanio == "grande" and len(capitanes) != 2:
        return JsonResponse(
            {"error": "Las naves grandes deben tener exactamente dos capitanes"},
            status=400
        )

    if len(tripulantes) > nave.capacidad:
        return JsonResponse(
            {"error": "La tripulación supera la capacidad de la nave"},
            status=400
        )

    usuarios_ids = capitanes + tripulantes
    if not usuarios_ids:
        return JsonResponse(
            {"error": "Debes indicar al menos un capitán o tripulante"},
            status=400
        )

    usuarios_existentes = set(
        Usuario.objects.filter(id__in=usuarios_ids).values_list("id", flat=True)
    )
    usuarios_faltantes = sorted(set(usuarios_ids) - usuarios_existentes)
    if usuarios_faltantes:
        return JsonResponse(
            {"error": f"Usuarios no encontrados: {usuarios_faltantes}"},
            status=404
        )

    usuarios_ocupados = list(
        Participacion.objects.filter(
            usuario_id__in=usuarios_ids,
            mision__estado="en_curso"
        ).values_list("usuario_id", flat=True).distinct()
    )
    if usuarios_ocupados:
        return JsonResponse(
            {"error": f"Usuarios no disponibles: {sorted(usuarios_ocupados)}"},
            status=400
        )

    nueva_mision = Mision.objects.create(
        descripcion=descripcion.strip(),
        nave=nave,
        estado="en_curso",
    )

    for usuario_id in capitanes:
        Participacion.objects.create(
            rol="capitan",
            mision=nueva_mision,
            usuario_id=usuario_id,
        )
    for usuario_id in tripulantes:
        Participacion.objects.create(
            rol="tripulante",
            mision=nueva_mision,
            usuario_id=usuario_id,
        )

    return JsonResponse(
        {
            "mensaje": "Misión asignada correctamente",
            "id": nueva_mision.id
        },
        status=201
    )


@csrf_exempt
def finalizarmision(request, id):
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


    if mision.estado != "en_curso":
        return JsonResponse(
            {"error": "Solo se pueden finalizar misiones en curso"},
            status=400
        )

    estado = datos.get("estado")
    if estado not in ["exito", "fracaso"]:
        return JsonResponse(
            {"error": "El estado debe ser 'exito' o 'fracaso'"},
            status=400
        )

    exoplanetas = datos.get("exoplanetas", [])
    if exoplanetas is None:
        exoplanetas = []
    if not isinstance(exoplanetas, list) or not all(isinstance(n, str) for n in exoplanetas):
        return JsonResponse(
            {"error": "exoplanetas debe ser una lista de nombres"},
            status=400
        )

    exoplanetas_limpios = [n.strip() for n in exoplanetas if n.strip()]
    if estado == "fracaso" and exoplanetas_limpios:
        return JsonResponse(
            {"error": "Solo se pueden registrar exoplanetas cuando la misión finaliza con éxito"},
            status=400
        )

    mision.estado = estado
    mision.fecha_fin = timezone.now()
    mision.save()

    if estado == "exito":
        for nombre in exoplanetas_limpios:
            Exoplaneta.objects.create(nombre=nombre, mision=mision)

    return JsonResponse(
        {
            "mensaje": "Misión finalizada correctamente",
            "id": mision.id,
            "estado": mision.estado
        }
    )



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

