"""Analisis por niveles: basico, intermedio y avanzado."""

from __future__ import annotations

import json
import logging
from typing import Any

from .cliente import get_client

__all__ = [
    "analizar_sentimiento_basico",
    "analizar_sentimiento_intermedio",
    "analizar_sentimiento_avanzado",
]

logger = logging.getLogger(__name__)

MODEL_NAME = "gpt-4o-mini"
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


def _crear_respuesta(prompt_sistema: str, texto: str) -> str:
    logger.debug("Llamando a OpenAI para analisis de sentimiento")
    client = get_client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": texto},
        ],
        temperature=0.0,
    )
    contenido = response.choices[0].message.content
    return contenido.strip() if contenido else ""


def _parsear_json_respuesta(contenido: str) -> dict[str, Any]:
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
            "Analiza el sentimiento del texto. Responde unicamente en formato JSON con: "
            "sentimiento, polaridad, emociones e intensidad."
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
            "Analiza el sentimiento del texto en profundidad. "
            "Responde unicamente en formato JSON con: sentimiento_global, polaridad, "
            "fragmentos, justificacion, tonalidad y recomendacion."
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
