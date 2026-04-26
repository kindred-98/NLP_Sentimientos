"""Analisis de sentimiento por lotes."""

from __future__ import annotations

from typing import Any

from .niveles import analizar_sentimiento_intermedio


def analizar_sentimiento_multitexto(textos: list[str]) -> dict[str, Any]:
    """Analiza una coleccion de textos y agrega estadisticas."""
    if not isinstance(textos, list):
        raise TypeError("La coleccion de textos debe ser una lista.")

    resultados = [analizar_sentimiento_intermedio(texto) for texto in textos]
    polaridades = [
        resultado.get("polaridad", 0)
        for resultado in resultados
        if isinstance(resultado.get("polaridad"), (int, float))
    ]

    estadisticas = {
        "total": len(resultados),
        "positivos": sum(1 for resultado in resultados if resultado.get("sentimiento") == "positivo"),
        "negativos": sum(1 for resultado in resultados if resultado.get("sentimiento") == "negativo"),
        "neutrales": sum(1 for resultado in resultados if resultado.get("sentimiento") == "neutral"),
        "polaridad_promedio": sum(polaridades) / len(polaridades) if polaridades else 0,
    }

    return {
        "resultados_individuales": resultados,
        "estadisticas": estadisticas,
    }
