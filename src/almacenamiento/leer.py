"""Lectura y consulta del historial de resultados."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

__all__ = ["listar_analisis", "leer_json", "leer_txt", "buscar_por_fecha"]

logger = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CARPETA_TXT = _BASE_DIR / "logs" / "txt"
DEFAULT_CARPETA_JSON = _BASE_DIR / "logs" / "json"

CARPETA_TXT = Path(os.getenv("NLP_RESULTADOS_TXT", str(DEFAULT_CARPETA_TXT)))
CARPETA_JSON = Path(os.getenv("NLP_RESULTADOS_JSON", str(DEFAULT_CARPETA_JSON)))


def listar_analisis() -> list[str]:
    """Lista los analisis almacenados."""
    logger.debug("Listando analisis en %s", CARPETA_JSON)
    archivos = sorted(CARPETA_JSON.glob("*.json"))
    return [archivo.name for archivo in archivos]


def leer_json(nombre: str) -> dict:
    """Lee un analisis almacenado en formato JSON."""
    logger.debug("Leyendo archivo JSON: %s", nombre)
    ruta = CARPETA_JSON / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo JSON: {nombre}")
    return json.loads(ruta.read_text(encoding="utf-8"))


def leer_txt(nombre: str) -> str:
    """Lee un analisis almacenado en formato TXT."""
    logger.debug("Leyendo archivo TXT: %s", nombre)
    ruta = CARPETA_TXT / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo TXT: {nombre}")
    return ruta.read_text(encoding="utf-8")


def buscar_por_fecha(fecha: str) -> list[str]:
    """Filtra analisis por fecha contenida en el nombre del archivo."""
    logger.debug("Buscando analisis con fecha: %s", fecha)
    return [nombre for nombre in listar_analisis() if fecha in nombre]
