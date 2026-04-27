"""Proveedor de modelos de lenguaje usando Ollama."""

from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

OLLAMA_MODEL: str = os.getenv("NLP_OLLAMA_MODEL", "qwen2.5:3b")


def generar_respuesta(
    prompt_sistema: str, texto: str, modelo: Optional[str] = None
) -> str:
    """Genera una respuesta usando Ollama."""
    modelo = modelo or OLLAMA_MODEL
    logger.debug("Llamando a Ollama (%s) para analisis de sentimiento", modelo)
    return _generar_ollama(prompt_sistema, texto, modelo)


def _generar_ollama(
    prompt_sistema: str, texto: str, modelo: str
) -> str:  # pragma: no cover
    from ollama import chat

    response = chat(
        model=modelo,
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": texto},
        ],
        options={"temperature": 0.0},
    )
    return response["message"]["content"].strip()
