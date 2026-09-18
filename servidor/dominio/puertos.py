"""
Puertos que el dominio necesita para consultar especies. La
infraestructura los implementa (ver csv_repositorio_especies.py);
el dominio no sabe si detras hay un CSV, una base de datos o un mock.

Son dos interfaces separadas en vez de una sola con todos los
metodos, porque el caso de uso de diagnosticar solo necesita
obtener una especie, y el de listar solo necesita el catalogo
completo.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from dominio.especie import Especie


class ProveedorDeEspecie(ABC):
    @abstractmethod
    def obtener_por_nombre(self, nombre: str) -> Optional[Especie]:
        """Devuelve la Especie si existe, o None si no esta soportada."""
        raise NotImplementedError


class CatalogoDeEspecies(ABC):
    @abstractmethod
    def listar_todas(self) -> List[Especie]:
        raise NotImplementedError
