# Proyecto_Galactico

## Modelos

La aplicación `bbdd_galactico` contiene usuarios, características, naves,
misiones y exoplanetas. Las características se asignan a los usuarios mediante
`CaracteristicaUsuario`, y los tripulantes de una misión mediante
`Participacion`, ambas con claves foráneas.

Cada nave tiene un capitán; las grandes tienen además un segundo capitán
distinto. Los capitanes forman parte de todas las misiones de su nave y ocupan
plazas, pero no se deben añadir como registros de `Participacion`. La relación
`mision.tripulantes` contiene únicamente los demás tripulantes.

Las capacidades y el número de capitanes se comprueban en la base de datos.
La capacidad efectiva y la ausencia de capitanes duplicados en la tripulación
se validan al guardar naves, misiones y participaciones mediante `save()` o
desde el administrador. No se deben modificar estas relaciones con `update()`,
`bulk_create()` ni `mision.tripulantes.add()`, porque omiten esa validación.
Estas comprobaciones entre tablas no garantizan la capacidad ante escrituras
simultáneas; para uso concurrente se necesita una gestión transaccional
apropiada para la base de datos elegida.

Para crear las tablas:

```shell
py manage.py migrate
```

Los modelos están registrados en el administrador de Django (`/admin/`).