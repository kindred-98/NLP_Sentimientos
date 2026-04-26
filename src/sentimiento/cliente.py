"""Inicializacion y acceso al cliente de OpenAI."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI

_client: OpenAI | None = None


def get_client() -> OpenAI:
    """Devuelve un cliente OpenAI reutilizable y configurado."""
    global _client

    if _client is not None:
        return _client

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta la variable de entorno OPENAI_API_KEY.")

    _client = OpenAI(api_key=api_key)
    return _client
