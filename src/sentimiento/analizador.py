"""Orquestacion del analisis de sentimiento."""

from __future__ import annotations

from typing import Any

from .niveles import (
    analizar_sentimiento_avanzado,
    analizar_sentimiento_basico,
    analizar_sentimiento_intermedio,
)


def analizar_texto(texto: str) -> dict[str, Any]:
    """Orquesta el analisis completo de un texto."""
    return {
        "texto": texto,
        "basico": analizar_sentimiento_basico(texto),
        "intermedio": analizar_sentimiento_intermedio(texto),
        "avanzado": analizar_sentimiento_avanzado(texto),
    }
