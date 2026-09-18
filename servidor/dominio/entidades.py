"""Objetos que representan una medicion y el resultado de evaluarla."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List

from dominio.especie import RangoOptimo


class EstadoParametro(str, Enum):
    BAJO = "BAJO"
    OPTIMO = "OPTIMO"
    ALTO = "ALTO"


class EstadoPlanta(str, Enum):
    SALUDABLE = "SALUDABLE"
    EN_RIESGO = "EN_RIESGO"
    CRITICO = "CRITICO"


@dataclass(frozen=True)
class Medicion:
    """Una lectura de humedad, luz y temperatura para una especie."""
    especie: str
    humedad: float
    luz: float
    temperatura: float


@dataclass(frozen=True)
class ParametroEvaluado:
    nombre: str
    valor: float
    unidad: str
    rango_optimo: RangoOptimo
    estado: EstadoParametro


@dataclass(frozen=True)
class Diagnostico:
    especie: str
    estado: EstadoPlanta
    parametros: List[ParametroEvaluado] = field(default_factory=list)
    recomendaciones: List[str] = field(default_factory=list)
