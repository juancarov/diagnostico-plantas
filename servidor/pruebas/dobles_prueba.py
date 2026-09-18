"""Dobles de prueba para no depender del CSV real ni de Flask."""

from typing import Dict, List, Optional

from dominio.especie import Especie, RangoOptimo


class RepositorioEspeciesFalso:
    """Los mismos puertos que RepositorioEspeciesCSV, pero en memoria."""

    def __init__(self, especies: Optional[Dict[str, Especie]] = None):
        self._especies = especies or {}

    def obtener_por_nombre(self, nombre: str) -> Optional[Especie]:
        return self._especies.get((nombre or "").strip().lower())

    def listar_todas(self) -> List[Especie]:
        return list(self._especies.values())


def especie_de_prueba(nombre: str = "sansevieria trifasciata ‘laurentii’") -> Especie:
    return Especie(
        nombre=nombre,
        humedad=RangoOptimo(20.0, 45.0),
        luz=RangoOptimo(200.0, 1500.0),
        temperatura=RangoOptimo(15.0, 29.0),
        nombre_comun="Lengua de suegra",
    )
