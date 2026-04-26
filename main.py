"""Punto de entrada principal del proyecto."""

from __future__ import annotations

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from sentimiento.analizador import analizar_texto


def main() -> None:
    """Ejecuta una demostracion minima del analizador modularizado."""
    texto = "El producto llego rapido, pero la calidad no es la esperada."
    print("Proyecto inicializado. Analizador modular disponible.")
    print(f"Funcion principal cargada: {analizar_texto.__name__}")
    print(f"Texto de ejemplo: {texto}")
    print("Usa analizar_texto(texto) desde main o desde la interfaz futura.")


if __name__ == "__main__":
    main()
