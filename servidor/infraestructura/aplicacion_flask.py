"""Arma la app Flask: instancia el repositorio, el servicio de
dominio y los casos de uso, y registra las rutas. Si el CSV cambia
por una base de datos, solo esta linea de aqui cambia."""

import os

from flask import Flask
from flask_cors import CORS

from aplicacion.diagnosticar_planta import DiagnosticarPlantaCasoDeUso
from aplicacion.listar_especies import ListarEspeciesCasoDeUso
from dominio.evaluador import (
    EvaluadorDeEstadoGlobal,
    EvaluadorHumedad,
    EvaluadorLuz,
    EvaluadorTemperatura,
    GeneradorDeRecomendaciones,
)
from dominio.servicio_diagnostico import ServicioDiagnostico
from infraestructura.csv_repositorio_especies import RepositorioEspeciesCSV
from presentacion.controladores import crear_blueprint

_RUTA_CSV_POR_DEFECTO = os.path.join(os.path.dirname(__file__), "especies.csv")


def crear_app(ruta_csv: str = _RUTA_CSV_POR_DEFECTO) -> Flask:
    app = Flask(__name__)
    CORS(app)  # para que el front, en otro origen, pueda consumir la API

    repositorio_especies = RepositorioEspeciesCSV(ruta_csv)

    servicio_diagnostico = ServicioDiagnostico(
        evaluador_humedad=EvaluadorHumedad(),
        evaluador_luz=EvaluadorLuz(),
        evaluador_temperatura=EvaluadorTemperatura(),
        evaluador_estado_global=EvaluadorDeEstadoGlobal(),
        generador_recomendaciones=GeneradorDeRecomendaciones(),
    )

    diagnosticar_cu = DiagnosticarPlantaCasoDeUso(
        proveedor_especie=repositorio_especies,
        servicio_diagnostico=servicio_diagnostico,
    )
    listar_especies_cu = ListarEspeciesCasoDeUso(catalogo=repositorio_especies)

    app.register_blueprint(crear_blueprint(diagnosticar_cu, listar_especies_cu))

    return app
