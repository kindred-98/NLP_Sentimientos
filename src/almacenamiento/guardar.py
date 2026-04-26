"""Persistencia de resultados en TXT y JSON."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

__all__ = ["guardar_resultado", "get_rutas_resultados"]

logger = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CARPETA_TXT = _BASE_DIR / "resultados" / "txt"
DEFAULT_CARPETA_JSON = _BASE_DIR / "resultados" / "json"

CARPETA_TXT = Path(os.getenv("NLP_RESULTADOS_TXT", str(DEFAULT_CARPETA_TXT)))
CARPETA_JSON = Path(os.getenv("NLP_RESULTADOS_JSON", str(DEFAULT_CARPETA_JSON)))


def get_rutas_resultados() -> tuple[Path, Path]:
    """Devuelve las rutas configuradas para TXT y JSON."""
    return CARPETA_TXT, CARPETA_JSON


def _crear_carpetas() -> None:
    CARPETA_TXT.mkdir(parents=True, exist_ok=True)
    CARPETA_JSON.mkdir(parents=True, exist_ok=True)


def _generar_nombre_base() -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return f"analisis_{timestamp}"


def _formatear_txt(texto_entrada: str, resultados: dict[str, Any], timestamp: str) -> str:
    basico = resultados.get("basico", {})
    intermedio = resultados.get("intermedio", {})
    avanzado = resultados.get("avanzado", {})

    lineas = [
        "=" * 60,
        f"ANALISIS DE SENTIMIENTO - {timestamp}",
        "=" * 60,
        "",
        "TEXTO ANALIZADO:",
        texto_entrada,
        "",
        f"RESULTADO BASICO: {basico.get('sentimiento', 'N/D')}",
        (
            "RESULTADO INTERMEDIO: "
            f"{intermedio.get('sentimiento', 'N/D')} | "
            f"polaridad: {intermedio.get('polaridad', 'N/D')} | "
            f"intensidad: {intermedio.get('intensidad', 'N/D')}"
        ),
        f"JUSTIFICACION: {avanzado.get('justificacion', 'N/D')}",
    ]
    return "\n".join(lineas)


def guardar_resultado(texto_entrada: str, resultados: dict[str, Any]) -> dict[str, str]:
    """Guarda resultados de analisis en disco."""
    logger.info("Guardando resultado de analisis")
    if not isinstance(texto_entrada, str):
        raise TypeError("El texto de entrada debe ser una cadena.")
    if not isinstance(resultados, dict):
        raise TypeError("Los resultados deben proporcionarse en un diccionario.")

    _crear_carpetas()

    nombre_base = _generar_nombre_base()
    timestamp_legible = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ruta_txt = CARPETA_TXT / f"{nombre_base}.txt"
    ruta_json = CARPETA_JSON / f"{nombre_base}.json"

    contenido_json = {
        "timestamp": timestamp_legible,
        "texto": texto_entrada,
        "basico": resultados.get("basico", {}),
        "intermedio": resultados.get("intermedio", {}),
        "avanzado": resultados.get("avanzado", {}),
    }

    ruta_txt.write_text(
        _formatear_txt(texto_entrada, resultados, timestamp_legible),
        encoding="utf-8",
    )
    ruta_json.write_text(
        json.dumps(contenido_json, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.info("Resultado guardado en %s y %s", ruta_txt, ruta_json)

    return {
        "txt": str(ruta_txt),
        "json": str(ruta_json),
    }
