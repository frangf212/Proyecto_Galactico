# Proyecto Galáctico – API REST

## 1. Descripción

API REST desarrollada con Django para gestionar usuarios, naves espaciales, misiones, participaciones y exoplanetas. La información se intercambia en formato JSON y se almacena en SQLite.

## 2. Modelos

- **Usuario:** nombre.
- **CaracteristicaUsuario:** característica asociada a un usuario.
- **Nave:** tamaño y capacidad de tripulantes.
- **Mision:** descripción, estado, fechas y nave asignada.
- **Participacion:** relaciona usuarios con misiones e indica su rol (capitán o tripulante).
- **Exoplaneta:** nombre y misión en la que se descubre.

## 3. Preparación y comprobaciones en PyCharm

1. Abrir el proyecto en PyCharm.
2. En **File > Settings > Project > Python Interpreter**, seleccionar el intérprete de la carpeta `.venv` del proyecto.
3. Abrir la pestaña **Terminal**, situada en la parte inferior de PyCharm.
4. Situarse en la carpeta `introduccion`, donde está `manage.py`. Si la terminal no está allí, entrar con `cd introduccion` desde la carpeta principal.
5. Ejecutar los siguientes comandos, uno por uno:

```bash
python -m pip install -r ../requirements.txt
python manage.py check
python manage.py migrate
python manage.py test galacticodb
```

`check` revisa la configuración del proyecto; `migrate` prepara la base de datos; `test` ejecuta las pruebas automáticas de la aplicación.

## 4. Factoría de datos

El archivo `galacticodb/testFactoria.py` contiene las funciones `crear_flota()` y `crear_misiones_y_exoplanetas()` para generar datos de prueba.

**Antes de ejecutarla, hay que corregir la factoría para que coincida con `models.py`:**

- `Usuario` solo tiene el campo `nombre`; quitar el argumento `tipo` al crear usuarios.
- `CaracteristicaUsuario` utiliza el campo `usuario`, no `user`.
- La relación inversa de las características se llama `caracteristicas`.
- `Nave.capacidad` representa únicamente el número máximo de tripulantes; asignar `cantidad_tripulantes`.
- `Exoplaneta` necesita una `mision`; asignar cada planeta a una misión existente.
- Los tests de `CrearFlotaTests` deben estar en `galacticodb/tests.py` para que Django los descubra automáticamente. Actualizar sus comprobaciones para que coincidan con los modelos y la capacidad de la nave.

Con las correcciones realizadas, desde la Terminal de PyCharm y dentro de `introduccion`, ejecutar:

```bash
python manage.py shell
```

Cuando aparezca el indicador `>>>`, ejecutar:

```python
from galacticodb.testFactoria import crear_flota, crear_misiones_y_exoplanetas
flota = crear_flota()
misiones, exoplanetas = crear_misiones_y_exoplanetas()
```

Para comprobar los registros generados:

```python
from galacticodb.models import Usuario, Nave, Mision, Exoplaneta, CaracteristicaUsuario
print("Usuarios:", Usuario.objects.count())
print("Naves:", Nave.objects.count())
print("Misiones:", Mision.objects.count())
print("Exoplanetas:", Exoplaneta.objects.count())
print("Características:", CaracteristicaUsuario.objects.count())
```

La factoría crea 30 naves (10 pequeñas, 10 medianas y 10 grandes), sus usuarios y características, 20 misiones y 30 exoplanetas. Ejecutarla una sola vez sobre la misma base de datos para evitar duplicados. Para salir de la consola: `exit()`.

## 5. Arrancar el servidor

Desde la Terminal de PyCharm, en la carpeta `introduccion`:

```bash
python manage.py runserver
```

La API estará disponible en `http://127.0.0.1:8000`.

## 6. Endpoints disponibles

| Método | URL | Función |
|---|---|---|
| GET | `/api/usuarios/` | Listar usuarios. |
| GET | `/api/usuario/{id}/` | Consultar un usuario. |
| POST | `/api/usuarios/crear/` | Crear un usuario. |
| PUT | `/api/usuarios/{id}/actualizar/` | Actualizar el nombre. |
| PATCH | `/api/usuarios/{id}/parcial/` | Modificar parcialmente el usuario. |
| DELETE | `/api/usuarios/{id}/eliminar/` | Eliminar un usuario si no tiene participaciones. |
| POST | `/api/misiones/asignar/` | Crear una misión y asignar capitanes y tripulantes. |
| POST | `/api/misiones/{id}/finalizar/` | Finalizar una misión y registrar exoplanetas si tiene éxito. |
| GET | `/api/misiones/{id}/tripulantes/` | Consultar la tripulación de una misión. |
| GET | `/api/capitanes/{id}/exoplanetas/` | Consultar los exoplanetas de las misiones del capitán. |

## 7. Probar los endpoints desde PyCharm

Se pueden probar con el cliente HTTP integrado de PyCharm:

1. En el panel del proyecto, hacer clic derecho sobre la carpeta `introduccion`.
2. Seleccionar **New > HTTP Request** y crear el archivo `pruebas.http`.
3. Copiar las peticiones siguientes. Para ejecutarlas, pulsar el icono verde que aparece junto a cada petición.

```http
### Listar usuarios
GET http://127.0.0.1:8000/api/usuarios/

### Consultar un usuario
GET http://127.0.0.1:8000/api/usuario/1/

### Crear usuario
POST http://127.0.0.1:8000/api/usuarios/crear/
Content-Type: application/json

{
  "nombre": "Francisco"
}

### Actualizar usuario
PUT http://127.0.0.1:8000/api/usuarios/1/actualizar/
Content-Type: application/json

{
  "nombre": "Francisco Actualizado"
}

### Actualizar parcialmente
PATCH http://127.0.0.1:8000/api/usuarios/1/parcial/
Content-Type: application/json

{
  "nombre": "Francisco Modificado"
}

### Eliminar usuario
DELETE http://127.0.0.1:8000/api/usuarios/1/eliminar/

### Asignar misión (ejemplo para una nave pequeña)
POST http://127.0.0.1:8000/api/misiones/asignar/
Content-Type: application/json

{
  "descripcion": "Exploración de Marte",
  "nave_id": 1,
  "capitanes": [1],
  "tripulantes": [2, 3, 4, 5]
}

### Consultar tripulantes de una misión
GET http://127.0.0.1:8000/api/misiones/1/tripulantes/

### Finalizar misión con éxito
POST http://127.0.0.1:8000/api/misiones/1/finalizar/
Content-Type: application/json

{
  "estado": "exito",
  "exoplanetas": ["Kepler-22b", "Proxima-b"]
}

### Consultar exoplanetas de un capitán
GET http://127.0.0.1:8000/api/capitanes/1/exoplanetas/
```

Los identificadores `1`, `2`, etc. son ejemplos: deben sustituirse por IDs existentes en la base de datos. Para probar el flujo de misiones, primero asignar una misión; después consultar sus tripulantes y finalizarla. Para consultar exoplanetas de un capitán, ese usuario debe haber participado como capitán en una misión.

**Nota:** una nave pequeña o mediana necesita exactamente un capitán; una grande necesita dos. El número de tripulantes no puede superar la capacidad de la nave. Los usuarios asignados no pueden estar ya en otra misión en curso.

## 8. Códigos HTTP principales

- `200`: petición correcta.
- `201`: recurso creado.
- `204`: recurso eliminado correctamente.
- `400`: datos incorrectos o regla de negocio incumplida.
- `404`: recurso no encontrado.
- `405`: método HTTP no permitido.

## 9. Evidencias de comprobación

Para documentar las pruebas, guardar capturas de PyCharm mostrando:

- La salida correcta de `python manage.py check`.
- El resultado de `python manage.py test galacticodb`.
- Los recuentos de objetos generados por la factoría.
- Las respuestas de los endpoints principales, incluyendo una respuesta correcta y algún error controlado.

---

Este README describe las funcionalidades y rutas presentes en el código del proyecto. La factoría debe corregirse según las indicaciones anteriores antes de ejecutarla, ya que el archivo original contiene referencias a campos y relaciones que no coinciden con los modelos actuales.

## 10. Alternativa: realizar las comprobaciones fuera de PyCharm

Si PyCharm no permite ejecutar los comandos o no funciona su cliente HTTP, se pueden hacer las mismas comprobaciones desde **PowerShell** y **Postman**.

### 10.1 Abrir PowerShell en la carpeta del proyecto

1. Abrir PowerShell.
2. Entrar en la carpeta donde se encuentra el proyecto. Por ejemplo:

```powershell
cd C:\Users\grand\Documents\Proyecto_Galactico\Colon_galactico
```

3. Activar el entorno virtual si todavía no aparece `(.venv)` al principio de la línea:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Entrar en la carpeta `introduccion`, donde está `manage.py`:

```powershell
cd introduccion
```

Si la estructura de carpetas es distinta, hay que situarse siempre en la carpeta que contiene `manage.py`.

### 10.2 Ejecutar las comprobaciones de Django

Ejecutar los comandos uno por uno:

```powershell
python -m pip install -r ..\requirements.txt
python manage.py check
python manage.py migrate
python manage.py test galacticodb
```

### 10.3 Crear los datos con la factoría

Una vez corregida la factoría según el apartado 4, abrir la consola:

```powershell
python manage.py shell
```

Los comandos que aparecen después de `>>>` son código Python; no deben escribirse directamente en PowerShell.

```python
from galacticodb.testFactoria import crear_flota, crear_misiones_y_exoplanetas
flota = crear_flota()
misiones, exoplanetas = crear_misiones_y_exoplanetas()
```

Para salir de la consola:

```python
exit()
```

### 10.4 Arrancar el servidor y probar con Postman

Desde PowerShell, en la carpeta que contiene `manage.py`, ejecutar:

```powershell
python manage.py runserver
```

Dejar esa ventana abierta. Abrir Postman, importar la colección `Proyecto_Galactico.postman_collection.json` si está disponible o crear las peticiones manualmente usando las URLs y los JSON del apartado 7. La dirección base es `http://127.0.0.1:8000`.

Si se utiliza Postman, sustituir los IDs de ejemplo por los identificadores reales generados por la factoría. Para probar el flujo completo, asignar primero una misión, consultar después sus tripulantes y finalmente finalizar esa misión.

**Importante:** PowerShell ejecuta comandos del sistema, como `python manage.py runserver`. Las instrucciones `import`, `print` y las llamadas a `crear_flota()` solo se ejecutan dentro de la consola de Django, después de ejecutar `python manage.py shell` y ver el indicador `>>>`.
