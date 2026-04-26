"""Persistencia de resultados en TXT y JSON."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
CARPETA_TXT = BASE_DIR / "resultados" / "txt"
CARPETA_JSON = BASE_DIR / "resultados" / "json"


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

    return {
        "txt": str(ruta_txt),
        "json": str(ruta_json),
    }
