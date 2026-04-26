"""Paquete de analisis de sentimiento."""

from __future__ import annotations

from .analizador import ResultadoAnalisis, analizar_texto
from .multitexto import analizar_sentimiento_multitexto
from .niveles import (
    analizar_sentimiento_avanzado,
    analizar_sentimiento_basico,
    analizar_sentimiento_intermedio,
)

__all__ = [
    "analizar_texto",
    "analizar_sentimiento_basico",
    "analizar_sentimiento_intermedio",
    "analizar_sentimiento_avanzado",
    "analizar_sentimiento_multitexto",
    "ResultadoAnalisis",
]

__version__ = "0.1.0"
