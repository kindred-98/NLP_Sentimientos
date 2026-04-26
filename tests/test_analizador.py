"""Tests unitarios para el analizador de sentimiento."""

from __future__ import annotations

import pytest

from sentimiento.analizador import ResultadoAnalisis, analizar_texto
from sentimiento.multitexto import analizar_sentimiento_multitexto
from sentimiento.niveles import (
    MAX_LONGITUD_TEXTO,
    analizar_sentimiento_avanzado,
    analizar_sentimiento_basico,
    analizar_sentimiento_intermedio,
)


def test_sentimiento_basico_devuelve_categoria(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "sentimiento.niveles._crear_respuesta", lambda prompt, texto: "positivo"
    )

    resultado = analizar_sentimiento_basico("Me ha gustado mucho")

    assert resultado["nivel"] == "basico"
    assert resultado["sentimiento"] == "positivo"


def test_sentimiento_basico_rechaza_texto_vacio() -> None:
    with pytest.raises(ValueError):
        analizar_sentimiento_basico("   ")


def test_sentimiento_basico_rechaza_tipo_invalido() -> None:
    with pytest.raises(TypeError):
        analizar_sentimiento_basico(12345)  # type: ignore[arg-type]


def test_sentimiento_basico_rechaza_longitud_excesiva() -> None:
    texto_largo = "x" * (MAX_LONGITUD_TEXTO + 1)
    with pytest.raises(ValueError, match="longitud maxima"):
        analizar_sentimiento_basico(texto_largo)


def test_sentimiento_intermedio_parsea_json(monkeypatch: pytest.MonkeyPatch) -> None:
    respuesta = (
        '{"sentimiento": "negativo", "polaridad": -0.6, '
        '"emociones": {"tristeza": 0.8}, "intensidad": "alta"}'
    )
    monkeypatch.setattr(
        "sentimiento.niveles._crear_respuesta", lambda prompt, texto: respuesta
    )

    resultado = analizar_sentimiento_intermedio("No me ha gustado nada")

    assert resultado["nivel"] == "intermedio"
    assert resultado["sentimiento"] == "negativo"
    assert resultado["polaridad"] == -0.6


def test_sentimiento_intermedio_devuelve_error_si_json_invalido(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "sentimiento.niveles._crear_respuesta",
        lambda prompt, texto: "respuesta libre",
    )

    resultado = analizar_sentimiento_intermedio("Texto ambiguo")

    assert resultado["nivel"] == "intermedio"
    assert "error" in resultado
    assert resultado["respuesta_raw"] == "respuesta libre"


def test_sentimiento_avanzado_parsea_respuesta(monkeypatch: pytest.MonkeyPatch) -> None:
    respuesta = (
        '{"sentimiento_global": "neutral", "polaridad": 0.0, '
        '"fragmentos": [], "justificacion": "Hay equilibrio.", '
        '"tonalidad": "formal", "recomendacion": "Seguir observando"}'
    )
    monkeypatch.setattr(
        "sentimiento.niveles._crear_respuesta", lambda prompt, texto: respuesta
    )

    resultado = analizar_sentimiento_avanzado("Texto neutro")

    assert resultado["nivel"] == "avanzado"
    assert resultado["sentimiento_global"] == "neutral"
    assert resultado["justificacion"] == "Hay equilibrio."


def test_analizar_texto_orquesta_tres_niveles(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "sentimiento.analizador.analizar_sentimiento_basico",
        lambda texto: {"nivel": "basico", "sentimiento": "positivo"},
    )
    monkeypatch.setattr(
        "sentimiento.analizador.analizar_sentimiento_intermedio",
        lambda texto: {
            "nivel": "intermedio",
            "sentimiento": "positivo",
            "polaridad": 0.5,
        },
    )
    monkeypatch.setattr(
        "sentimiento.analizador.analizar_sentimiento_avanzado",
        lambda texto: {"nivel": "avanzado", "sentimiento_global": "positivo"},
    )

    resultado: ResultadoAnalisis = analizar_texto("Buen producto")

    assert resultado["texto"] == "Buen producto"
    assert resultado["basico"]["nivel"] == "basico"
    assert resultado["intermedio"]["polaridad"] == 0.5
    assert resultado["avanzado"]["sentimiento_global"] == "positivo"


def test_analizar_texto_devuelve_resultado_analisis(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "sentimiento.analizador.analizar_sentimiento_basico",
        lambda texto: {"nivel": "basico", "sentimiento": "positivo"},
    )
    monkeypatch.setattr(
        "sentimiento.analizador.analizar_sentimiento_intermedio",
        lambda texto: {
            "nivel": "intermedio",
            "sentimiento": "positivo",
            "polaridad": 0.5,
        },
    )
    monkeypatch.setattr(
        "sentimiento.analizador.analizar_sentimiento_avanzado",
        lambda texto: {"nivel": "avanzado", "sentimiento_global": "positivo"},
    )

    resultado = analizar_texto("Buen producto")

    assert isinstance(resultado, ResultadoAnalisis)


def test_multitexto_calcula_estadisticas(monkeypatch: pytest.MonkeyPatch) -> None:
    respuestas = [
        {"sentimiento": "positivo", "polaridad": 0.8},
        {"sentimiento": "negativo", "polaridad": -0.4},
        {"sentimiento": "neutral", "polaridad": 0.0},
    ]

    def falso_intermedio(texto: str) -> dict:
        return respuestas.pop(0)

    monkeypatch.setattr(
        "sentimiento.multitexto.analizar_sentimiento_intermedio", falso_intermedio
    )

    resultado = analizar_sentimiento_multitexto(["a", "b", "c"])

    assert resultado["estadisticas"]["total"] == 3
    assert resultado["estadisticas"]["positivos"] == 1
    assert resultado["estadisticas"]["negativos"] == 1
    assert resultado["estadisticas"]["neutrales"] == 1
    assert resultado["estadisticas"]["polaridad_promedio"] == pytest.approx(
        0.1333333333
    )


def test_multitexto_rechaza_tipo_invalido() -> None:
    with pytest.raises(TypeError):
        analizar_sentimiento_multitexto("no es una lista")  # type: ignore[arg-type]


def test_multitexto_con_lista_vacia() -> None:
    resultado = analizar_sentimiento_multitexto([])

    assert resultado["estadisticas"]["total"] == 0
    assert resultado["estadisticas"]["positivos"] == 0
    assert resultado["estadisticas"]["negativos"] == 0
    assert resultado["estadisticas"]["neutrales"] == 0
    assert resultado["estadisticas"]["polaridad_promedio"] == 0.0
