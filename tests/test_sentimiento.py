"""Tests para sentimiento/niveles.py y sentimiento/proveedor.py."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest


class TestProveedor:
    """Tests para modulo proveedor."""

    def test_ollama_model_tiene_valor_defecto(self) -> None:
        from sentimiento.proveedor import OLLAMA_MODEL

        assert OLLAMA_MODEL == "qwen2.5:3b"

    def test_generar_respuesta_sin_modelo(self) -> None:
        from sentimiento.proveedor import generar_respuesta

        with patch("sentimiento.proveedor._generar_ollama") as mock:
            mock.return_value = "respuesta"
            resultado = generar_respuesta("prompt", "texto")
            assert resultado == "respuesta"
            mock.assert_called_once_with("prompt", "texto", "qwen2.5:3b")

    def test_generar_respuesta_con_modelo_explicito(self) -> None:
        from sentimiento.proveedor import generar_respuesta

        with patch("sentimiento.proveedor._generar_ollama") as mock:
            mock.return_value = "respuesta"
            generar_respuesta("prompt", "texto", modelo="llama3")
            mock.assert_called_once_with("prompt", "texto", "llama3")

    def test_generar_respuesta_pasa_prompt_sistema(self) -> None:
        from sentimiento.proveedor import generar_respuesta

        with patch("sentimiento.proveedor._generar_ollama") as mock:
            mock.return_value = "neutral"
            generar_respuesta("Eres un analisis de sentimientos", "el texto")
            args = mock.call_args[0]
            assert args[0] == "Eres un analisis de sentimientos"
            assert args[1] == "el texto"


def _test_generar_respuesta_usa_modelo_defecto(self) -> None:
    from sentimiento.proveedor import generar_respuesta, OLLAMA_MODEL

    with patch("sentimiento.proveedor._generar_ollama") as mock:
        mock.return_value = "positivo"
        generar_respuesta("prompt", "texto")
        _, _, modelo = mock.call_args[0]
        assert modelo == OLLAMA_MODEL


class TestNiveles:
    """Tests para modulo niveles."""

    def test_parsear_json_respuesta_vacia(self) -> None:
        from sentimiento.niveles import _parsear_json_respuesta

        with pytest.raises(json.JSONDecodeError):
            _parsear_json_respuesta("")

    def test_parsear_json_respuesta_con_json_embed(self) -> None:
        from sentimiento.niveles import _parsear_json_respuesta

        resultado = _parsear_json_respuesta('texto {"clave": "valor"} texto')
        assert resultado == {"clave": "valor"}

    def test_validar_texto_rechaza_vacio(self) -> None:
        from sentimiento.niveles import _validar_texto

        with pytest.raises(ValueError, match="no puede estar vacio"):
            _validar_texto("")

    def test_validar_texto_rechaza_longitud_excesiva(self) -> None:
        from sentimiento.niveles import _validar_texto

        texto_largo = "a" * 10001
        with pytest.raises(ValueError, match="longitud maxima"):
            _validar_texto(texto_largo)

    def test_basico_con_mock_proveedor(self) -> None:
        from sentimiento.niveles import analizar_sentimiento_basico

        with patch("sentimiento.niveles._crear_respuesta") as mock:
            mock.return_value = "positivo"
            resultado = analizar_sentimiento_basico("texto de prueba")
            assert resultado["sentimiento"] == "positivo"

    def test_basico_maneja_error_json(self) -> None:
        from sentimiento.niveles import analizar_sentimiento_basico

        with patch("sentimiento.niveles._crear_respuesta") as mock:
            mock.return_value = "no es json"
            resultado = analizar_sentimiento_basico("texto")
            assert resultado["sentimiento"] == "no es json"

    def test_intermedio_con_mock(self) -> None:
        from sentimiento.niveles import analizar_sentimiento_intermedio

        with patch("sentimiento.niveles._crear_respuesta") as mock:
            mock.return_value = (
                '{"sentimiento": "negativo", "polaridad": -0.75, "intensidad": "alta"}'
            )
            resultado = analizar_sentimiento_intermedio("texto de prueba")
            assert resultado["sentimiento"] == "negativo"
            assert resultado["polaridad"] == -0.75

    def test_intermedio_maneja_error_parseo(self) -> None:
        from sentimiento.niveles import analizar_sentimiento_intermedio

        with patch("sentimiento.niveles._crear_respuesta") as mock:
            mock.return_value = "invalid json"
            resultado = analizar_sentimiento_intermedio("texto")
            assert "error" in resultado

    def test_avanzado_con_mock(self) -> None:
        from sentimiento.niveles import analizar_sentimiento_avanzado

        with patch("sentimiento.niveles._crear_respuesta") as mock:
            mock.return_value = (
                '{"sentimiento_global": "neutral", "polaridad": 0.0, '
                '"justificacion": "texto neutro", "tonalidad": "neutro"}'
            )
            resultado = analizar_sentimiento_avanzado("texto de prueba")
            assert resultado["sentimiento_global"] == "neutral"

    def test_avanzado_maneja_error_parseo(self) -> None:
        from sentimiento.niveles import analizar_sentimiento_avanzado

        with patch("sentimiento.niveles._crear_respuesta") as mock:
            mock.return_value = "respuesta invalida"
            resultado = analizar_sentimiento_avanzado("texto")
            assert "error" in resultado
