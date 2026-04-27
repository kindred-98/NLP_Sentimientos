"""Tests unitarios para persistencia y lectura de resultados."""

from __future__ import annotations

import shutil
import uuid
from pathlib import Path

import pytest

from almacenamiento import guardar as guardar_mod
from almacenamiento import leer as leer_mod


@pytest.fixture
def almacenamiento_temporal(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[Path, Path]:
    base_tmp = Path(__file__).resolve().parent / "_tmp" / uuid.uuid4().hex
    carpeta_txt = base_tmp / "txt"
    carpeta_json = base_tmp / "json"
    monkeypatch.setattr(guardar_mod, "CARPETA_TXT", carpeta_txt)
    monkeypatch.setattr(guardar_mod, "CARPETA_JSON", carpeta_json)
    monkeypatch.setattr(leer_mod, "CARPETA_TXT", carpeta_txt)
    monkeypatch.setattr(leer_mod, "CARPETA_JSON", carpeta_json)
    try:
        yield carpeta_txt, carpeta_json
    finally:
        if base_tmp.exists():
            shutil.rmtree(base_tmp, ignore_errors=True)


def _resultados_ejemplo() -> dict:
    return {
        "basico": {"sentimiento": "negativo"},
        "intermedio": {
            "sentimiento": "negativo",
            "polaridad": -0.4,
            "intensidad": "media",
        },
        "avanzado": {"justificacion": "Predomina la decepcion por la calidad."},
    }


def test_guardar_txt_crea_archivo(almacenamiento_temporal: tuple[Path, Path]) -> None:
    carpeta_txt, _ = almacenamiento_temporal

    rutas = guardar_mod.guardar_resultado("Texto de prueba", _resultados_ejemplo())

    ruta_txt = Path(rutas["txt"])
    assert ruta_txt.exists()
    assert ruta_txt.parent == carpeta_txt
    assert "RESULTADO BASICO" in ruta_txt.read_text(encoding="utf-8")


def test_guardar_json_crea_archivo(almacenamiento_temporal: tuple[Path, Path]) -> None:
    _, carpeta_json = almacenamiento_temporal

    rutas = guardar_mod.guardar_resultado("Texto de prueba", _resultados_ejemplo())

    ruta_json = Path(rutas["json"])
    assert ruta_json.exists()
    assert ruta_json.parent == carpeta_json
    assert '"texto": "Texto de prueba"' in ruta_json.read_text(encoding="utf-8")


def test_listar_analisis_devuelve_archivos_json(
    almacenamiento_temporal: tuple[Path, Path],
) -> None:
    guardar_mod.guardar_resultado("Uno", _resultados_ejemplo())

    analisis = leer_mod.listar_analisis()

    assert len(analisis) == 1
    assert analisis[0].endswith(".json")


def test_leer_json_recupera_contenido(
    almacenamiento_temporal: tuple[Path, Path],
) -> None:
    rutas = guardar_mod.guardar_resultado("Uno", _resultados_ejemplo())

    contenido = leer_mod.leer_json(Path(rutas["json"]).name)

    assert contenido["texto"] == "Uno"
    assert contenido["intermedio"]["polaridad"] == -0.4


def test_leer_txt_recupera_contenido(
    almacenamiento_temporal: tuple[Path, Path],
) -> None:
    rutas = guardar_mod.guardar_resultado("Uno", _resultados_ejemplo())

    contenido = leer_mod.leer_txt(Path(rutas["txt"]).name)

    assert "TEXTO ANALIZADO:" in contenido
    assert "Uno" in contenido


def test_buscar_por_fecha_filtra_resultados(
    almacenamiento_temporal: tuple[Path, Path],
) -> None:
    rutas = guardar_mod.guardar_resultado("Uno", _resultados_ejemplo())
    nombre = Path(rutas["json"]).name
    fecha = nombre.replace("analisis_", "")[:10]

    encontrados = leer_mod.buscar_por_fecha(fecha)

    assert nombre in encontrados


def test_leer_json_lanza_error_si_no_existe(
    almacenamiento_temporal: tuple[Path, Path],
) -> None:
    with pytest.raises(FileNotFoundError):
        leer_mod.leer_json("inexistente.json")


def test_guardar_resultado_rechaza_texto_no_string(
    almacenamiento_temporal: tuple[Path, Path],
) -> None:
    with pytest.raises(TypeError, match="texto de entrada debe ser una cadena"):
        guardar_mod.guardar_resultado(123, {"basico": {}})


def test_guardar_resultado_rechaza_resultados_no_dict(
    almacenamiento_temporal: tuple[Path, Path],
) -> None:
    with pytest.raises(TypeError, match="resultados deben proporcionarse en un diccionario"):
        guardar_mod.guardar_resultado("texto", "no es dict")


def test_leer_txt_lanza_error_si_no_existe(
    almacenamiento_temporal: tuple[Path, Path],
) -> None:
    with pytest.raises(FileNotFoundError):
        leer_mod.leer_txt("inexistente.txt")
