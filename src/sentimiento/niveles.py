"""Analisis por niveles: basico, intermedio y avanzado."""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from .proveedor import generar_respuesta as _crear_respuesta

__all__ = [
    "analizar_sentimiento_basico",
    "analizar_sentimiento_intermedio",
    "analizar_sentimiento_avanzado",
]

logger = logging.getLogger(__name__)

MAX_LONGITUD_TEXTO = 10000


class AnalisisError(Exception):
    """Error durante el analisis de sentimiento."""


def _validar_texto(texto: str) -> str:
    if not isinstance(texto, str):
        raise TypeError("El texto a analizar debe ser una cadena.")
    texto_limpio = texto.strip()
    if not texto_limpio:
        raise ValueError("El texto a analizar no puede estar vacio.")
    if len(texto_limpio) > MAX_LONGITUD_TEXTO:
        raise ValueError(
            f"El texto excede la longitud maxima permitida ({MAX_LONGITUD_TEXTO} caracteres)."
        )
    return texto_limpio


def _resumen_texto(texto: str, limite: int = 100) -> str:
    return texto if len(texto) <= limite else f"{texto[:limite]}..."


def _parsear_json_respuesta(contenido: str) -> dict[str, Any]:
    contenido = contenido.strip()
    if not contenido:
        raise json.JSONDecodeError("Respuesta vacia", "", 0)
    match = re.search(r"\{.*\}", contenido, re.DOTALL)
    if match:
        contenido = match.group(0)
    return json.loads(contenido)


def analizar_sentimiento_basico(texto: str) -> dict[str, Any]:
    """Analiza un texto en nivel basico."""
    logger.info("Iniciando analisis basico")
    texto_limpio = _validar_texto(texto)
    contenido = _crear_respuesta(
        (
            "Analiza el sentimiento del texto. "
            "Responde solo con una palabra: positivo, negativo o neutral."
        ),
        texto_limpio,
    )

    resultado = {
        "nivel": "basico",
        "sentimiento": contenido.lower(),
        "texto_original": _resumen_texto(texto_limpio),
    }
    logger.debug("Resultado basico: %s", resultado)
    return resultado


def analizar_sentimiento_intermedio(texto: str) -> dict[str, Any]:
    """Analiza un texto en nivel intermedio."""
    logger.info("Iniciando analisis intermedio")
    texto_limpio = _validar_texto(texto)
    contenido = _crear_respuesta(
        (
            "You are a sentiment analysis assistant. Analyze the text and respond ONLY "
            "with valid JSON. No text before or after. Format: "
            '{"sentimiento": "positivo|negativo|neutral", "polaridad": -1.0 to 1.0, '
            '"emociones": {"alegria": 0.0 to 1.0, "tristeza": 0.0 to 1.0, '
            '"enojo": 0.0 to 1.0, "sorpresa": 0.0 to 1.0, "miedo": 0.0 to 1.0}, '
            '"intensidad": "baja|media|alta"}. '
            'Example: {"sentimiento": "positivo", "polaridad": 0.8, '
            '"emociones": {"alegria": 0.9, "tristeza": 0.0, "enojo": 0.0, '
            '"sorpresa": 0.1, "miedo": 0.0}, "intensidad": "alta"}'
        ),
        texto_limpio,
    )

    try:
        resultado = _parsear_json_respuesta(contenido)
    except json.JSONDecodeError as exc:
        logger.warning("No se pudo parsear respuesta JSON: %s", exc)
        return {
            "nivel": "intermedio",
            "error": "No se pudo parsear la respuesta en formato JSON.",
            "respuesta_raw": contenido,
            "texto_original": _resumen_texto(texto_limpio),
        }

    resultado["nivel"] = "intermedio"
    resultado["texto_original"] = _resumen_texto(texto_limpio)
    logger.debug("Resultado intermedio: %s", resultado)
    return resultado


def analizar_sentimiento_avanzado(texto: str) -> dict[str, Any]:
    """Analiza un texto en nivel avanzado."""
    logger.info("Iniciando analisis avanzado")
    texto_limpio = _validar_texto(texto)
    contenido = _crear_respuesta(
        (
            "You are a deep sentiment analysis assistant. Respond ONLY with valid JSON. "
            "No text before or after. Format: "
            '{"sentimiento_global": "positivo|negativo|neutral", '
            '"polaridad": -1.0 to 1.0, '
            '"justificacion": "brief explanation of the analysis", '
            '"tonalidad": "formal|coloquial|agresivo|entusiasta|neutro", '
            '"recomendacion": "action or advice based on sentiment", '
            '"fragmentos": [{"texto": "relevant text", '
            '"sentimiento_individual": "positivo|negativo|neutral"}]}. '
            'Example: {"sentimiento_global": "positivo", "polaridad": 0.7, '
            '"justificacion": "Positive language with enthusiastic tone.", '
            '"tonalidad": "entusiasta", '
            '"recomendacion": "Continue this approach.", '
            '"fragmentos": [{"texto": "excellent product", '
            '"sentimiento_individual": "positivo"}]}'
        ),
        texto_limpio,
    )

    try:
        resultado = _parsear_json_respuesta(contenido)
    except json.JSONDecodeError as exc:
        logger.warning("No se pudo parsear respuesta JSON: %s", exc)
        return {
            "nivel": "avanzado",
            "error": "No se pudo parsear la respuesta en formato JSON.",
            "respuesta_raw": contenido,
            "texto_original": _resumen_texto(texto_limpio),
        }

    resultado["nivel"] = "avanzado"
    resultado["texto_original"] = _resumen_texto(texto_limpio)
    logger.debug("Resultado avanzado: %s", resultado)
    return resultado
