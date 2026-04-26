"""Tests unitarios para el cliente de OpenAI."""

from __future__ import annotations

import os

import pytest

from sentimiento.cliente import get_client


def test_get_client_lanza_error_sin_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(os, "getenv", lambda key: None)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        get_client()


def test_get_client_rechaza_clave_vacia(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        os, "getenv", lambda key: "" if key == "OPENAI_API_KEY" else None
    )

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        get_client()


def test_get_client_reutiliza_instancia(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeClient:
        pass

    fake = FakeClient()

    def fake_getenv(key: str) -> str | None:
        if key == "OPENAI_API_KEY":
            return "fake-key"
        return None

    monkeypatch.setattr(os, "getenv", fake_getenv)

    import sentimiento.cliente as cliente_mod

    cliente_mod._client = None

    monkeypatch.setattr("openai.OpenAI.__init__", lambda self, api_key: None)
    monkeypatch.setattr("sentimiento.cliente.OpenAI", lambda api_key: fake)

    resultado1 = get_client()
    resultado2 = get_client()

    assert resultado1 is resultado2
    assert resultado1 is fake
