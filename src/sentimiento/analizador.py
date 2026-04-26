"""Orquestacion del analisis de sentimiento."""

from __future__ import annotations

import logging

from .niveles import (
    analizar_sentimiento_avanzado,
    analizar_sentimiento_basico,
    analizar_sentimiento_intermedio,
)

__all__ = ["analizar_texto", "ResultadoAnalisis"]

logger = logging.getLogger(__name__)


class ResultadoAnalisis(dict):
    """Representa el resultado completo de un analisis."""


def analizar_texto(texto: str) -> ResultadoAnalisis:
    """Orquesta el analisis completo de un texto."""
    logger.info("Iniciando analisis completo del texto")
    resultado = ResultadoAnalisis(
        {
            "texto": texto,
            "basico": analizar_sentimiento_basico(texto),
            "intermedio": analizar_sentimiento_intermedio(texto),
            "avanzado": analizar_sentimiento_avanzado(texto),
        }
    )
    logger.info("Analisis completo finalizado")
    return resultado
