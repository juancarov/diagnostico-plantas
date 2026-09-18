"""Caso de uso: devuelve todas las especies soportadas, para que el
front pueble el selector dinamicamente."""

from typing import List

from dominio.especie import Especie
from dominio.puertos import CatalogoDeEspecies


class ListarEspeciesCasoDeUso:
    def __init__(self, catalogo: CatalogoDeEspecies):
        self._catalogo = catalogo

    def ejecutar(self) -> List[Especie]:
        return self._catalogo.listar_todas()
