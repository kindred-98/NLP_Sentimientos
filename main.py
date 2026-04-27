"""Punto de entrada al proyecto."""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "src"))

from src.menu import menu_principal

if __name__ == "__main__":
    menu_principal()
