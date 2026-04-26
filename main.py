"""Punto de entrada principal del proyecto con CLI."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%H:%M:%S",
)

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from sentimiento.analizador import ResultadoAnalisis, analizar_texto
from almacenamiento.guardar import guardar_resultado
from almacenamiento.leer import listar_analisis


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analizador de sentimiento con IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "texto",
        nargs="*",
        help="Texto a analizar. Si se omite, entra en modo interactivo.",
    )
    parser.add_argument(
        "-n",
        "--nivel",
        choices=["basico", "intermedio", "avanzado"],
        default="avanzado",
        help="Nivel de analisis a ejecutar (default: avanzado)",
    )
    parser.add_argument(
        "-g",
        "--guardar",
        action="store_true",
        help="Guardar resultado tras el analisis",
    )
    parser.add_argument(
        "-l",
        "--listar",
        action="store_true",
        help="Listar analisis guardados en el historial",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Activar modo verbose (debug logs)",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.listar:
        historial = listar_analisis()
        if not historial:
            print("No hay analisis guardados.")
            return
        print(f"{len(historial)} analisis en el historial:")
        for nombre in historial:
            print(f"  - {nombre}")
        return

    if args.texto:
        texto = " ".join(args.texto)
    else:
        print("Modo interactivo. Escribe un texto y presiona Enter (Ctrl+C para salir).")
        try:
            texto = input("\nTexto: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo.")
            return

    if not texto:
        print("Error: el texto no puede estar vacio.")
        sys.exit(1)

    try:
        resultado: ResultadoAnalisis = analizar_texto(texto)
    except Exception as exc:
        print(f"Error durante el analisis: {exc}")
        sys.exit(1)

    basico = resultado.get("basico", {})
    intermedio = resultado.get("intermedio", {})
    avanzado = resultado.get("avanzado", {})

    print("\n" + "=" * 60)
    print("RESULTADO DEL ANALISIS")
    print("=" * 60)
    print(f"Basico:       {basico.get('sentimiento', 'N/D')}")
    print(
        f"Intermedio:   {intermedio.get('sentimiento', 'N/D')} "
        f"(polaridad {intermedio.get('polaridad', 'N/D')})"
    )
    print(f"Avanzado:     {avanzado.get('sentimiento_global', 'N/D')}")
    print(f"Justificacion: {avanzado.get('justificacion', 'N/D')}")
    print("=" * 60)

    if args.guardar:
        try:
            rutas = guardar_resultado(texto, resultado)
            print("\nGuardado en:")
            print(f"  TXT: {rutas['txt']}")
            print(f"  JSON: {rutas['json']}")
        except Exception as exc:
            print(f"Error al guardar: {exc}")
            sys.exit(1)


if __name__ == "__main__":
    main()
