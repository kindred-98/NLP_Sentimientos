"""Analisis de sentimiento por lotes."""

from __future__ import annotations

import logging
from typing import Any

from .niveles import analizar_sentimiento_intermedio

__all__ = ["analizar_sentimiento_multitexto"]

logger = logging.getLogger(__name__)


def analizar_sentimiento_multitexto(textos: list[str]) -> dict[str, Any]:
    """Analiza una coleccion de textos y agrega estadisticas."""
    logger.info("Iniciando analisis multitexto con %d textos", len(textos))
    if not isinstance(textos, list):
        raise TypeError("La coleccion de textos debe ser una lista.")

    if not textos:
        logger.warning("La lista de textos esta vacia")
        return {
            "resultados_individuales": [],
            "estadisticas": {
                "total": 0,
                "positivos": 0,
                "negativos": 0,
                "neutrales": 0,
                "polaridad_promedio": 0.0,
            },
        }

    resultados = [analizar_sentimiento_intermedio(texto) for texto in textos]
    polaridades = [
        resultado.get("polaridad", 0)
        for resultado in resultados
        if isinstance(resultado.get("polaridad"), (int, float))
    ]

    estadisticas = {
        "total": len(resultados),
        "positivos": sum(1 for r in resultados if r.get("sentimiento") == "positivo"),
        "negativos": sum(1 for r in resultados if r.get("sentimiento") == "negativo"),
        "neutrales": sum(1 for r in resultados if r.get("sentimiento") == "neutral"),
        "polaridad_promedio": sum(polaridades) / len(polaridades) if polaridades else 0.0,
    }
    logger.info("Analisis multitexto completado: %s", estadisticas)
    return {
        "resultados_individuales": resultados,
        "estadisticas": estadisticas,
    }
