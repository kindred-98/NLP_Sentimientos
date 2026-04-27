"""Menu de entrada del Analizador de Sentimiento."""

from __future__ import annotations

import sys
from pathlib import Path


def menu_principal() -> None:
    while True:
        print("\n" + "=" * 50)
        print("   ANALIZADOR DE SENTIMIENTO - NLP")
        print("=" * 50)
        print("  1. Ejecutar GUI (Interfaz Grafica)")
        print("  2. Ejecutar CLI (Linea de comandos)")
        print("  3. Salir")
        print("=" * 50)
        opcion = input("Selecciona una opcion (1-3): ").strip()

        if opcion == "1":
            ejecutar_gui()
        elif opcion == "2":
            ejecutar_cli()
        elif opcion == "3":
            print("\n¡Hasta luego!")
            break
        else:
            print("\nOpcion invalida. Intenta de nuevo.")


def ejecutar_gui() -> None:
    print("\nIniciando GUI (cierra la ventana para volver al menu)...")
    try:
        import subprocess  # noqa: B404

        BASE_DIR = Path(__file__).resolve().parent.parent
        subprocess.run([sys.executable, str(BASE_DIR / "gui.py")], check=True)  # noqa: B603
    except Exception as exc:
        print(f"Error al iniciar GUI: {exc}")


def ejecutar_cli() -> None:
    from sentimiento.analizador import ResultadoAnalisis, analizar_texto
    from almacenamiento.guardar import guardar_resultado
    from almacenamiento.leer import listar_analisis
    import argparse
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    parser = argparse.ArgumentParser(description="Analizador de sentimiento con IA")
    parser.add_argument("texto", nargs="*", help="Texto a analizar")
    parser.add_argument(
        "-n",
        "--nivel",
        choices=["basico", "intermedio", "avanzado"],
        default="avanzado",
    )
    parser.add_argument("-g", "--guardar", action="store_true")
    parser.add_argument("-l", "--listar", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.listar:
        historial = listar_analisis()
        print(
            f"{len(historial)} analisis guardados"
            if historial
            else "No hay analisis guardados."
        )
        return

    if args.texto:
        texto = " ".join(args.texto)
    else:
        texto = input("Texto a analizar: ").strip()
        if not texto:
            print("Error: el texto no puede estar vacio.")
            return

    try:
        resultado: ResultadoAnalisis = analizar_texto(texto)
    except Exception as exc:
        print(f"Error: {exc}")
        return

    basico = resultado.get("basico", {})
    intermedio = resultado.get("intermedio", {})
    avanzado = resultado.get("avanzado", {})

    print("\n" + "=" * 50)
    print("RESULTADO")
    print("=" * 50)
    print(f"Basico: {basico.get('sentimiento', 'N/D')}")
    print(
        f"Intermedio: {intermedio.get('sentimiento', 'N/D')} (polaridad {intermedio.get('polaridad', 'N/D')})"
    )
    print(f"Avanzado: {avanzado.get('sentimiento_global', 'N/D')}")
    print(f"Justificacion: {avanzado.get('justificacion', 'N/D')}")

    if args.guardar:
        rutas = guardar_resultado(texto, resultado)
        print(f"Guardado en: {rutas['json']}")


if __name__ == "__main__":
    menu_principal()
