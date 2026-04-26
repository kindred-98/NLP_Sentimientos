"""Paquete de analisis de sentimiento."""

from __future__ import annotations

from .guardar import guardar_resultado, get_rutas_resultados
from .leer import buscar_por_fecha, leer_json, leer_txt, listar_analisis

__all__ = [
    "guardar_resultado",
    "get_rutas_resultados",
    "listar_analisis",
    "leer_json",
    "leer_txt",
    "buscar_por_fecha",
]

__version__ = "0.1.0"
