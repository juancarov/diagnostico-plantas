"""Rutas HTTP: reciben el request, lo pasan por dtos.py, llaman al
caso de uso y traducen el resultado (o la excepcion) a JSON."""

from flask import Blueprint, jsonify, request

from aplicacion.diagnosticar_planta import DiagnosticarPlantaCasoDeUso
from aplicacion.listar_especies import ListarEspeciesCasoDeUso
from dominio.excepciones import EspecieNoSoportadaError, ParametroInvalidoError
from presentacion.dtos import diagnostico_a_json, especies_a_json, medicion_desde_request


def crear_blueprint(
    diagnosticar_cu: DiagnosticarPlantaCasoDeUso,
    listar_especies_cu: ListarEspeciesCasoDeUso,
) -> Blueprint:
    bp = Blueprint("api", __name__, url_prefix="/api/v1")

    @bp.route("/diagnosticos", methods=["POST"])
    def diagnosticar():
        payload = request.get_json(silent=True) or {}

        try:
            medicion = medicion_desde_request(payload)
            diagnostico = diagnosticar_cu.ejecutar(medicion)
        except ParametroInvalidoError as error:
            return (
                jsonify(
                    {
                        "error": "PARAMETRO_INVALIDO",
                        "mensaje": str(error),
                        "detalle": {"campo": error.campo},
                    }
                ),
                400,
            )
        except EspecieNoSoportadaError as error:
            return (
                jsonify(
                    {
                        "error": "ESPECIE_NO_SOPORTADA",
                        "mensaje": str(error),
                        "detalle": {"especie": error.especie},
                    }
                ),
                404,
            )

        return jsonify(diagnostico_a_json(diagnostico)), 200

    @bp.route("/especies", methods=["GET"])
    def listar_especies():
        especies = listar_especies_cu.ejecutar()
        return jsonify(especies_a_json(especies)), 200

    return bp
