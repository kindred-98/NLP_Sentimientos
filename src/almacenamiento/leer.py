"""Lectura y consulta del historial de resultados."""

from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CARPETA_TXT = BASE_DIR / "resultados" / "txt"
CARPETA_JSON = BASE_DIR / "resultados" / "json"


def _asegurar_carpetas() -> None:
    CARPETA_TXT.mkdir(parents=True, exist_ok=True)
    CARPETA_JSON.mkdir(parents=True, exist_ok=True)


def listar_analisis() -> list[str]:
    """Lista los analisis almacenados."""
    _asegurar_carpetas()
    archivos = sorted(CARPETA_JSON.glob("*.json"))
    return [archivo.name for archivo in archivos]


def leer_json(nombre: str) -> dict:
    """Lee un analisis almacenado en formato JSON."""
    _asegurar_carpetas()
    ruta = CARPETA_JSON / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo JSON: {nombre}")
    return json.loads(ruta.read_text(encoding="utf-8"))


def leer_txt(nombre: str) -> str:
    """Lee un analisis almacenado en formato TXT."""
    _asegurar_carpetas()
    ruta = CARPETA_TXT / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo TXT: {nombre}")
    return ruta.read_text(encoding="utf-8")


def buscar_por_fecha(fecha: str) -> list[str]:
    """Filtra analisis por fecha contenida en el nombre del archivo."""
    _asegurar_carpetas()
    return [nombre for nombre in listar_analisis() if fecha in nombre]
