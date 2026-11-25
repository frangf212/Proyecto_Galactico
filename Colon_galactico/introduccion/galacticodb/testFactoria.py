from django.db import transaction
from django.test import TestCase
from faker import Faker

from .models import CaraterísticasUsuarios, Exoplanetas, Misiones, Nave, Usuario


CARACTERISTICAS = [
    "Misiones largas",
    "Explorador de cortas distancias",
    "Conflictivo",
    "Cocinero",
    "Mantenimiento",
]


def crear_usuarios(cantidad, tipo, fake):
    usuarios = []

    for numero_usuario in range(cantidad):
        usuario = Usuario(nombre=fake.name(), tipo=tipo)
        usuario.save()

        caracteristica = CaraterísticasUsuarios(
            user=usuario,
            caracteristica=fake.random_element(CARACTERISTICAS),
        )
        caracteristica.save()
        usuarios.append(usuario)

    return usuarios



def crear_flota():
    """Crea 10 naves de cada tamaño con su dotación y una característica por usuario."""
    fake = Faker("es_ES")
    flota = []

    tamanios = ["Pequeña", "Mediana", "Grande"]

    for tamanio in tamanios:
        for numero_nave in range(10):
            if tamanio == "Pequeña":
                cantidad_capitanes = 1
                cantidad_tripulantes = 4
            elif tamanio == "Mediana":
                cantidad_capitanes = 1
                cantidad_tripulantes = fake.random_int(8, 10)
            else:
                cantidad_capitanes = 2
                cantidad_tripulantes = fake.random_int(11, 30)

            nave = Nave(
                tamanio=tamanio,
                capacidad=cantidad_capitanes + cantidad_tripulantes,
            )
            nave.save()
            dotacion = {
                "nave": nave,
                "capitanes": crear_usuarios(cantidad_capitanes, "Capitán", fake),
                "tripulantes": crear_usuarios(cantidad_tripulantes, "Tripulante", fake),
            }
            flota.append(dotacion)

    return flota


@transaction.atomic
def crear_misiones_y_exoplanetas():
    naves = list(Nave.objects.all())
    if not naves:
        raise ValueError("Es necesario crear naves antes de generar misiones.")

    fake = Faker("es_ES")
    misiones = []
    exoplanetas = []

    for numero_mision in range(1, 21):
        mision = Misiones(
            descripcion=f"Expedición espacial {numero_mision}",
            nave=fake.random_element(naves),
        )
        mision.save()
        misiones.append(mision)

    for numero_planeta in range(1, 31):
        planeta = Exoplanetas(nombre=f"{fake.first_name()}-{numero_planeta}")
        planeta.save()
        exoplanetas.append(planeta)

    return misiones, exoplanetas


class CrearFlotaTests(TestCase):
    def test_crea_30_naves_con_dotaciones_y_caracteristicas_validas(self):
        flota = crear_flota()

        self.assertEqual(len(flota), 30)
        self.assertEqual(Nave.objects.count(), 30)
        self.assertEqual(Usuario.objects.count(), CaraterísticasUsuarios.objects.count())

        for tamanio in ["Pequeña", "Mediana", "Grande"]:
            self.assertEqual(Nave.objects.filter(tamanio=tamanio).count(), 10)

        usuarios_creados = []
        for dotacion in flota:
            capitanes = len(dotacion["capitanes"])
            tripulantes = len(dotacion["tripulantes"])

            if dotacion["nave"].tamanio == "Pequeña":
                self.assertEqual((capitanes, tripulantes), (1, 4))
            elif dotacion["nave"].tamanio == "Mediana":
                self.assertEqual(capitanes, 1)
                self.assertIn(tripulantes, range(8, 11))
            else:
                self.assertEqual(capitanes, 2)
                self.assertIn(tripulantes, range(11, 31))

            self.assertEqual(
                dotacion["nave"].capacidad,
                capitanes + tripulantes,
            )
            for usuario in dotacion["capitanes"]:
                self.assertEqual(usuario.tipo, "Capitán")
            for usuario in dotacion["tripulantes"]:
                self.assertEqual(usuario.tipo, "Tripulante")
            for usuario in dotacion["capitanes"] + dotacion["tripulantes"]:
                self.assertTrue(usuario.nombre)
                self.assertNotIn(usuario.pk, usuarios_creados)
                usuarios_creados.append(usuario.pk)
                self.assertIn(usuario.usuarios.get().caracteristica, CARACTERISTICAS)

        self.assertEqual(len(usuarios_creados), Usuario.objects.count())

    def test_crea_20_misiones_y_30_exoplanetas(self):
        nave = Nave(tamanio="Pequeña", capacidad=5)
        nave.save()

        misiones, exoplanetas = crear_misiones_y_exoplanetas()

        self.assertEqual(len(misiones), 20)
        self.assertEqual(len(exoplanetas), 30)
        self.assertEqual(Misiones.objects.count(), 20)
        self.assertEqual(Exoplanetas.objects.count(), 30)
        for mision in misiones:
            self.assertEqual(mision.nave, nave)
            self.assertTrue(mision.descripcion)
        for planeta in exoplanetas:
            self.assertTrue(planeta.nombre)

    def test_no_crea_misiones_ni_planetas_si_no_hay_naves(self):
        with self.assertRaisesMessage(ValueError, "Es necesario crear naves"):
            crear_misiones_y_exoplanetas()

        self.assertEqual(Misiones.objects.count(), 0)
        self.assertEqual(Exoplanetas.objects.count(), 0)