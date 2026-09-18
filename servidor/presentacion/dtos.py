"""Valida el JSON que llega y lo convierte a objetos de dominio, y
convierte los objetos de dominio de vuelta a JSON para la respuesta."""

from typing import Any, Dict, List

from dominio.entidades import Diagnostico, Medicion
from dominio.especie import Especie
from dominio.excepciones import ParametroInvalidoError

# Rangos fisicos (lo que un sensor real podria reportar), no los
# rangos ideales de cada especie -- esos ya los compara el dominio.
_RANGOS_FISICOS = {
    "humedad": (0.0, 100.0),      # % de humedad del sustrato
    "luz": (0.0, 100000.0),       # lux; generoso para luz solar directa
    "temperatura": (-40.0, 80.0),  # C
}


def _parsear_numero(payload: Dict[str, Any], campo: str) -> float:
    if campo not in payload or payload[campo] in (None, ""):
        raise ParametroInvalidoError(campo, "ausente")

    valor_crudo = payload[campo]
    try:
        valor = float(valor_crudo)
    except (TypeError, ValueError):
        raise ParametroInvalidoError(campo, "no numerico")

    minimo, maximo = _RANGOS_FISICOS[campo]
    if valor < minimo or valor > maximo:
        raise ParametroInvalidoError(campo, "fuera del rango fisicamente posible")

    return valor


def medicion_desde_request(payload: Dict[str, Any]) -> Medicion:
    especie = payload.get("especie")
    if not especie or not isinstance(especie, str):
        raise ParametroInvalidoError("especie", "ausente")

    humedad = _parsear_numero(payload, "humedad")
    luz = _parsear_numero(payload, "luz")
    temperatura = _parsear_numero(payload, "temperatura")

    return Medicion(especie=especie, humedad=humedad, luz=luz, temperatura=temperatura)


def diagnostico_a_json(diagnostico: Diagnostico) -> Dict[str, Any]:
    return {
        "especie": diagnostico.especie,
        "estado": diagnostico.estado.value,
        "parametros": [
            {
                "nombre": p.nombre,
                "valor": p.valor,
                "unidad": p.unidad,
                "rangoOptimo": [p.rango_optimo.minimo, p.rango_optimo.maximo],
                "estado": p.estado.value,
            }
            for p in diagnostico.parametros
        ],
        "recomendaciones": diagnostico.recomendaciones,
    }


def especie_a_json(especie: Especie) -> Dict[str, Any]:
    return {
        "nombre": especie.nombre,
        "nombreComun": especie.nombre_comun,
        "rangos": {
            "humedad": [especie.humedad.minimo, especie.humedad.maximo],
            "luz": [especie.luz.minimo, especie.luz.maximo],
            "temperatura": [especie.temperatura.minimo, especie.temperatura.maximo],
        },
    }


def especies_a_json(especies: List[Especie]) -> List[Dict[str, Any]]:
    return [especie_a_json(e) for e in especies]
