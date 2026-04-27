"""Constructor de widgets de la interfaz."""

from __future__ import annotations

import tkinter as tk
from tkinter import scrolledtext, ttk

from .tema import (
    COLUMNS,
    FONT_BASE,
    FONT_BOLD,
    FONT_CONSOLA,
    HIST_COLUMNS,
    ROW_DESFAVORABLE,
    ROW_FAVORABLE,
    TAG_DESFAVORABLE,
    TAG_FAVORABLE,
    TREE_COL_W,
    TREE_TEXT_COL_W,
)


class Widgets:
    def __init__(self, parent: tk.Tk | tk.Widget) -> None:
        self.parent = parent
        self._crear_widgets()

    def _crear_widgets(self) -> None:
        container = ttk.Frame(self.parent, padding="10")
        container.pack(fill=tk.BOTH, expand=True)

        self._crear_encabezado(container)
        self._crear_entrada_texto(container)
        self._crear_botones(container)
        self._crear_pestanas(container)
        self._crear_leyenda(container)
        self._crear_estado(container)

    def _crear_encabezado(self, container: ttk.Frame) -> None:
        header = ttk.Frame(container)
        header.pack(fill=tk.X, anchor=tk.W, pady=(0, 10))
        ttk.Label(
            header,
            text="ANALISIS DE SENTIMIENTO - LOCAL",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT)

    def _crear_entrada_texto(self, container: ttk.Frame) -> None:
        input_frame = ttk.LabelFrame(
            container,
            text="📝 Texto a analizar",
            padding=10,
        )
        input_frame.pack(fill=tk.BOTH, pady=(0, 10))

        text_border = tk.Frame(input_frame, relief="sunken", borderwidth=2, bg="white")
        text_border.pack(fill=tk.BOTH, expand=True)

        scroll = ttk.Scrollbar(text_border)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_input = tk.Text(
            text_border,
            height=4,
            font=("Segoe UI", 9),
            wrap=tk.WORD,
            bd=0,
            bg="white",
            yscrollcommand=scroll.set,
            foreground="black",
            insertbackground="black",
        )
        self.txt_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.txt_input.yview)

    def _crear_botones(self, container: ttk.Frame) -> None:
        botones = ttk.Frame(container)
        botones.pack(fill=tk.X, pady=(0, 10))

        self.btn_analizar = tk.Button(
            botones,
            text="🔍 ANALIZAR SENTIMIENTO",
            bg="#dcdad5",
            relief="raised",
            borderwidth=2,
        )
        self.btn_analizar.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_limpiar = tk.Button(
            botones,
            text="🧹 LIMPIAR",
            bg="#dcdad5",
            relief="raised",
            borderwidth=2,
        )
        self.btn_limpiar.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_guardar = tk.Button(
            botones,
            text="💾 GUARDAR",
            bg="#dcdad5",
            relief="raised",
            borderwidth=2,
        )
        self.btn_guardar.pack(side=tk.LEFT)

    def _crear_pestanas(self, container: ttk.Frame) -> None:
        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.tab_tabla = ttk.Frame(self.notebook, padding=5)
        self.tab_json = ttk.Frame(self.notebook)
        self.tab_just = ttk.Frame(self.notebook)
        self.tab_historial = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_tabla, text="📊 Resultados por Nivel")
        self.notebook.add(self.tab_json, text="📋 Analisis Detallado")
        self.notebook.add(self.tab_just, text="💡 Justificacion y Recomendacion")
        self.notebook.add(self.tab_historial, text="📜 Historial")

        self._crear_tree_resultados()
        self._crear_text_json()
        self._crear_text_justificacion()
        self._crear_historial()

    def _crear_tree_resultados(self) -> None:
        self.tree = ttk.Treeview(
            self.tab_tabla, columns=COLUMNS, show="headings", height=6
        )
        for c in COLUMNS:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.tag_configure(TAG_FAVORABLE, background=ROW_FAVORABLE)
        self.tree.tag_configure(TAG_DESFAVORABLE, background=ROW_DESFAVORABLE)

    def _crear_text_json(self) -> None:
        self.txt_json = scrolledtext.ScrolledText(
            self.tab_json, font=FONT_CONSOLA, bg="white", wrap=tk.WORD
        )
        self.txt_json.pack(fill=tk.BOTH, expand=True)

    def _crear_text_justificacion(self) -> None:
        self.txt_just = tk.Text(self.tab_just, font=FONT_BASE, wrap=tk.WORD)
        self.txt_just.pack(fill=tk.BOTH, expand=True)

    def _crear_historial(self) -> None:
        tree_frame = ttk.Frame(self.tab_historial)
        tree_frame.grid(row=0, column=0, sticky="nsew")
        self.tab_historial.columnconfigure(0, weight=1)
        self.tab_historial.rowconfigure(0, weight=1)

        scroll = ttk.Scrollbar(tree_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_hist = ttk.Treeview(
            tree_frame,
            columns=HIST_COLUMNS,
            show="headings",
            height=8,
            yscrollcommand=scroll.set,
        )
        for c in HIST_COLUMNS:
            self.tree_hist.heading(c, text=c.capitalize())
            self.tree_hist.column(
                c,
                width=TREE_COL_W if c != "texto_resumido" else TREE_TEXT_COL_W,
                anchor=tk.CENTER,
            )
        self.tree_hist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.tree_hist.yview)

        hist_btn = ttk.Frame(self.tab_historial)
        hist_btn.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        self.btn_cargar_hist = ttk.Button(
            hist_btn, text="Cargar Historial", command=None
        )
        self.btn_cargar_hist.pack(side=tk.LEFT, padx=(0, 5))
        self.btn_limpiar_hist = ttk.Button(hist_btn, text="Limpiar", command=None)
        self.btn_limpiar_hist.pack(side=tk.LEFT)

    def _crear_leyenda(self, container: ttk.Frame) -> None:
        frame_card = ttk.LabelFrame(
            container,
            text="¿Qué significa la polaridad?",
            padding=10,
        )
        frame_card.pack(fill=tk.X, pady=(0, 5))

        label_pos = tk.Label(
            frame_card,
            text="🟢 POSITIVA (+0.00 a +1.00): El texto expresa emociones positivas",
            fg="#008000",
            anchor="w",
            bg="#dcdad5",
        )
        label_pos.pack(fill=tk.X)

        label_neg = tk.Label(
            frame_card,
            text="🔴 NEGATIVA (-1.00 a -0.00): El texto expresa emociones negativas",
            fg="#D00000",
            anchor="w",
            bg="#dcdad5",
        )
        label_neg.pack(fill=tk.X)

        label_neu = tk.Label(
            frame_card,
            text="⚪ NEUTRAL (0.00): El texto no muestra emociones fuertes",
            fg="#808080",
            anchor="w",
            bg="#dcdad5",
        )
        label_neu.pack(fill=tk.X)

    def _crear_estado(self, container: ttk.Frame) -> None:
        status = ttk.Frame(container)
        status.pack(fill=tk.X, anchor=tk.W, pady=(5, 0))

        self.lbl_status = ttk.Label(status, text="Listo.")
        self.lbl_status.pack(side=tk.LEFT)

        self.auto_guardar = tk.BooleanVar(value=True)
        ttk.Checkbutton(status, text="Auto-guardar", variable=self.auto_guardar).pack(
            side=tk.RIGHT
        )


def construir_ventana(parent: tk.Tk) -> Widgets:
    """Construye todos los widgets y los devuelve."""
    return Widgets(parent)
