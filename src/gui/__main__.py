"""Interfaz grafica del analizador de sentimiento."""

from __future__ import annotations

import json
import logging
import sys
import threading
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import tkinter as tk
from tkinter import messagebox, ttk

from sentimiento.niveles import (
    analizar_sentimiento_avanzado,
    analizar_sentimiento_basico,
    analizar_sentimiento_intermedio,
)
from gui.tema import aplicar_tema, configurar_ventana
from gui.widgets import construir_ventana
from almacenamiento.guardar import guardar_resultado
from almacenamiento.leer import leer_json, listar_analisis

logger = logging.getLogger(__name__)


class GUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        configurar_ventana(self)
        self.title("Analisis de Sentimiento - Local")
        self.configure(bg="#dcdad5")

        style = ttk.Style()
        aplicar_tema(style)

        self._w = construir_ventana(self)
        self._ultimo_resultado: dict = {}
        self._analizando = False

        self._w.btn_analizar.config(command=self._analizar)
        self._vincular_botones()
        self._cargar_historial()

    def _vincular_botones(self) -> None:
        parent = self._w.parent
        for w in parent.winfo_children():
            if isinstance(w, ttk.Frame):
                for b in w.winfo_children():
                    if isinstance(b, ttk.Button):
                        txt = b.cget("text")
                        if txt == "LIMPIAR":
                            b.config(command=self._limpiar)
                        elif txt == "GUARDAR":
                            b.config(command=self._guardar)
                        elif txt == "Cargar Historial":
                            b.config(command=self._cargar_historial)
                        elif txt == "Limpiar":
                            b.config(command=self._limpiar_historial)

    def _analizar(self) -> None:
        texto = self._w.txt_input.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "Ingrese un texto para analizar.")
            return
        if self._analizando:
            return

        self._analizando = True
        self._w.btn_analizar.config(state="disabled")
        self._w.lbl_status.config(text="Analizando...")

        threading.Thread(target=self._proceso_ia, args=(texto,), daemon=True).start()

    def _proceso_ia(self, texto: str) -> None:
        self.after(0, self._limpiar_ui)

        try:
            res_b = analizar_sentimiento_basico(texto)
            sent_b = str(res_b.get("sentimiento", "")).upper()
            self.after(0, self._insertar, "Basico", sent_b, "-", "-")

            res_i = analizar_sentimiento_intermedio(texto)
            sent_i = str(res_i.get("sentimiento", "")).upper()
            self.after(
                0,
                self._insertar,
                "Intermedio",
                sent_i,
                str(res_i.get("polaridad", "N/D")),
                str(res_i.get("intensidad", "N/D")),
            )

            res_a = analizar_sentimiento_avanzado(texto)
            sent_a = str(res_a.get("sentimiento_global", "")).upper()
            self.after(
                0,
                self._insertar,
                "Avanzado",
                sent_a,
                str(res_a.get("polaridad", "N/D")),
                "-",
            )

            self._ultimo_resultado = {
                "timestamp": datetime.now().isoformat(),
                "texto_analizado": texto,
                "basico": res_b,
                "intermedio": res_i,
                "avanzado": res_a,
            }

            self.after(0, self._llenar_datos, res_a)

            if self._w.auto_guardar.get():
                self.after(0, self._auto_guardar)

        except Exception as e:
            logger.error("Error en analisis: %s", str(e))
            self.after(
                0,
                lambda err=e: messagebox.showerror("Error", f"Ocurrio un error: {err}"),
            )

        finally:
            self.after(0, self._finalizar)

    def _limpiar_ui(self) -> None:
        for item in self._w.tree.get_children():
            self._w.tree.delete(item)
        self._w.txt_json.delete("1.0", tk.END)
        self._w.txt_just.delete("1.0", tk.END)

    def _insertar(
        self, nivel: str, sentimiento: str, polaridad: str, intensidad: str
    ) -> None:
        tag = ""
        if "POSITIVO" in sentimiento:
            tag = "favorable"
        elif "NEGATIVO" in sentimiento:
            tag = "desfavorable"
        self._w.tree.insert(
            "",
            tk.END,
            values=(nivel, sentimiento, polaridad, intensidad),
            tags=(tag,) if tag else (),
        )

    def _llenar_datos(self, res_a: dict) -> None:
        self._w.txt_json.delete("1.0", tk.END)
        self._w.txt_json.insert(
            tk.END,
            json.dumps(self._ultimo_resultado, indent=4, ensure_ascii=False),
        )
        self._w.txt_just.delete("1.0", tk.END)
        self._w.txt_just.insert(
            tk.END,
            f"JUSTIFICACION:\n{res_a.get('justificacion', 'N/D')}\n\n"
            f"RECOMENDACION:\n{res_a.get('recomendacion', 'N/D')}\n\n"
            f"TONALIDAD:\n{res_a.get('tonalidad', 'N/D')}",
        )

    def _auto_guardar(self) -> None:
        try:
            rutas = guardar_resultado(
                self._ultimo_resultado.get("texto_analizado", ""),
                self._ultimo_resultado,
            )
            self._w.lbl_status.config(text=f"Guardado en {rutas['json']}")
            self._cargar_historial()
        except Exception as e:
            logger.warning("Auto-guardado fallido: %s", e)

    def _finalizar(self) -> None:
        self._analizando = False
        self._w.btn_analizar.config(state="normal")
        self._w.lbl_status.config(text="Analisis completado.")

    def _limpiar(self) -> None:
        self._w.txt_input.delete("1.0", tk.END)
        self._limpiar_ui()
        self._ultimo_resultado = {}
        self._w.lbl_status.config(text="Listo.")

    def _guardar(self) -> None:
        if not self._ultimo_resultado:
            messagebox.showwarning("Aviso", "Realiza un analisis antes de guardar.")
            return
        try:
            rutas = guardar_resultado(
                self._ultimo_resultado.get("texto_analizado", ""),
                self._ultimo_resultado,
            )
            messagebox.showinfo(
                "Guardado",
                f"Guardado en:\nTXT: {rutas['txt']}\nJSON: {rutas['json']}",
            )
            self._cargar_historial()
            self._w.lbl_status.config(text="Guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def _cargar_historial(self) -> None:
        self._w.tree_hist.delete(*self._w.tree_hist.get_children())
        try:
            archivos = listar_analisis()
            for archivo in archivos:
                try:
                    datos = leer_json(archivo)
                    ts = datos.get("timestamp", archivo)
                    texto = datos.get("texto", "")
                    resumido = (texto[:50] + "...") if len(texto) > 50 else texto
                    sent = datos.get("basico", {}).get("sentimiento", "N/D")
                    self._w.tree_hist.insert("", tk.END, values=(ts, resumido, sent))
                except Exception:
                    continue
            if archivos:
                self._w.lbl_status.config(text=f"Historial: {len(archivos)} analisis.")
        except Exception as e:
            logger.warning("No se pudo cargar el historial: %s", e)

    def _limpiar_historial(self) -> None:
        self._w.tree_hist.delete(*self._w.tree_hist.get_children())
        self._w.lbl_status.config(text="Historial limpiado.")


if __name__ == "__main__":
    app = GUI()
    app.mainloop()
