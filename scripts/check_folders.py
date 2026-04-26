"""Verifica que existan las carpetas requeridas del proyecto."""

from __future__ import annotations

from pathlib import Path


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    required_dirs = [
        base_dir / "src" / "almacenamiento",
        base_dir / "src" / "sentimiento",
        base_dir / "src" / "resultados" / "txt",
        base_dir / "src" / "resultados" / "json",
        base_dir / "tests",
        base_dir / "docs",
    ]

    missing = [str(path.relative_to(base_dir)) for path in required_dirs if not path.exists()]
    if missing:
        raise SystemExit(f"Faltan carpetas requeridas: {', '.join(missing)}")

    print("Estructura de carpetas verificada correctamente.")


if __name__ == "__main__":
    main()
