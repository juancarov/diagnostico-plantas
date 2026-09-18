"""Prueba el caso de uso inyectandole un repositorio falso en vez
del real, para comprobar que no depende de la implementacion CSV."""

import unittest

from aplicacion.diagnosticar_planta import DiagnosticarPlantaCasoDeUso
from dominio.entidades import Medicion
from dominio.evaluador import (
    EvaluadorDeEstadoGlobal,
    EvaluadorHumedad,
    EvaluadorLuz,
    EvaluadorTemperatura,
    GeneradorDeRecomendaciones,
)
from dominio.excepciones import EspecieNoSoportadaError
from dominio.servicio_diagnostico import ServicioDiagnostico
from pruebas.dobles_prueba import RepositorioEspeciesFalso, especie_de_prueba


class PruebaDiagnosticarPlantaCasoDeUso(unittest.TestCase):
    def setUp(self):
        self.servicio = ServicioDiagnostico(
            evaluador_humedad=EvaluadorHumedad(),
            evaluador_luz=EvaluadorLuz(),
            evaluador_temperatura=EvaluadorTemperatura(),
            evaluador_estado_global=EvaluadorDeEstadoGlobal(),
            generador_recomendaciones=GeneradorDeRecomendaciones(),
        )

    def test_diagnostica_una_especie_soportada(self):
        especie = especie_de_prueba("sansevieria")
        repo_falso = RepositorioEspeciesFalso({"sansevieria": especie})
        caso_de_uso = DiagnosticarPlantaCasoDeUso(repo_falso, self.servicio)

        medicion = Medicion("sansevieria", humedad=32.5, luz=850, temperatura=21.0)
        diagnostico = caso_de_uso.ejecutar(medicion)

        self.assertEqual(diagnostico.especie, "sansevieria")

    def test_especie_no_registrada_lanza_excepcion_de_dominio(self):
        repo_falso_vacio = RepositorioEspeciesFalso({})
        caso_de_uso = DiagnosticarPlantaCasoDeUso(repo_falso_vacio, self.servicio)

        medicion = Medicion("planta-inexistente", humedad=10, luz=10, temperatura=10)

        with self.assertRaises(EspecieNoSoportadaError):
            caso_de_uso.ejecutar(medicion)


if __name__ == "__main__":
    unittest.main()
