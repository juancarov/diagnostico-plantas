"""Excepciones de dominio. No tienen codigo HTTP a proposito -- eso
se traduce en la capa de presentacion."""


class EspecieNoSoportadaError(Exception):
    def __init__(self, especie: str):
        self.especie = especie
        super().__init__(f"Especie no soportada: {especie!r}")


class ParametroInvalidoError(Exception):
    """Un parametro esta ausente, no es numerico, o esta fuera del
    rango fisicamente posible."""

    def __init__(self, campo: str, motivo: str):
        self.campo = campo
        self.motivo = motivo
        super().__init__(f"Parametro invalido: {campo} ({motivo})")
