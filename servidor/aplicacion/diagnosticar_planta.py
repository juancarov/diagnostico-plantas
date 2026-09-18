"""Caso de uso: recibe una Medicion, resuelve su Especie a traves
del puerto ProveedorDeEspecie, y delega la evaluacion al dominio."""

from dominio.entidades import Diagnostico, Medicion
from dominio.excepciones import EspecieNoSoportadaError
from dominio.puertos import ProveedorDeEspecie
from dominio.servicio_diagnostico import ServicioDiagnostico


class DiagnosticarPlantaCasoDeUso:
    def __init__(
        self,
        proveedor_especie: ProveedorDeEspecie,
        servicio_diagnostico: ServicioDiagnostico,
    ):
        self._proveedor_especie = proveedor_especie
        self._servicio_diagnostico = servicio_diagnostico

    def ejecutar(self, medicion: Medicion) -> Diagnostico:
        especie = self._proveedor_especie.obtener_por_nombre(medicion.especie)
        if especie is None:
            raise EspecieNoSoportadaError(medicion.especie)
        return self._servicio_diagnostico.diagnosticar(especie, medicion)
