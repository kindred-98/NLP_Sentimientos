"""Tema visual estilo Windows XP para la interfaz."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def aplicar_tema(style: ttk.Style) -> None:
    """Aplica el tema estilo Windows XP a todos los widgets."""
    style.theme_use("winnative")

    style.configure("TFrame", background=BG, relief="flat")
    style.configure("TLabel", background=BG, font=FONT_BASE, foreground=FG)
    style.configure("TButton", font=FONT_BASE, padding=2, background=BG)
    style.configure("TNotebook", background=BG, tabposition="nw", borderwidth=1)
    style.configure(
        "TNotebook.Tab",
        font=FONT_BASE,
        padding=(4, 2),
        background="#E1DED8",
    )
    style.configure("TLabelframe", background=BG, borderwidth=2, relief="groove")
    style.configure(
        "TLabelframe.Label",
        background=BG,
        font=FONT_BOLD,
        foreground=FG,
    )
    style.configure(
        "Treeview",
        font=FONT_BASE,
        rowheight=20,
        borderwidth=1,
        relief="sunken",
    )
    style.configure("Treeview.Heading", font=FONT_BOLD, background=BG)
    style.configure("TCheckbutton", background=BG, font=FONT_BASE)

    style.map(
        "TButton",
        foreground=[("disabled", "#808080")],
        background=[("active", BG), ("!active", BG)],
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", BG), ("active", "#D6D3CD")],
        expand=[("selected", [0, 0, 0, 1])],
    )


# --- COLORES ---
BG = "#dcdad5"
WHITE = "white"
FG = "black"
FG_POSITIVO = "#008000"
FG_NEGATIVO = "#D00000"
FG_NEUTRAL = "#808080"
TEXTO_BG = "white"
ROW_FAVORABLE = "#ECFBF0"
ROW_DESFAVORABLE = "#FCE8E6"

# --- FUENTES ---
FONT_BASE = ("Tahoma", 8)
FONT_BOLD = ("Tahoma", 8, "bold")
FONT_TITLE = ("Arial", 10, "bold")
FONT_CONSOLA = ("Consolas", 8)
FONT_JSON = ("Consolas", 8)
FONT_SEGOE = ("Segoe UI", 9)

# --- DIMENSIONES ---
WINDOW_W = 800
WINDOW_H = 700
WINDOW_MIN_W = 770
WINDOW_MIN_H = 600
TEXT_HEIGHT = 4
TREE_ROWS = 6
TREE_HIST_ROWS = 8
TREE_COL_W = 150
TREE_TEXT_COL_W = 300
COLUMNS = ("nivel", "sentimiento", "polaridad", "intensidad")
HIST_COLUMNS = ("fecha", "texto_resumido", "sentimiento")

# --- ESTILOS DE TAGS PARA TREEVIEW ---
TAG_FAVORABLE = "favorable"
TAG_DESFAVORABLE = "desfavorable"


def configurar_ventana(ventana: tk.Tk) -> None:
    """Configura las dimensiones de la ventana."""
    ventana.geometry(f"{WINDOW_W}x{WINDOW_H}")
    ventana.minsize(WINDOW_MIN_W, WINDOW_MIN_H)
