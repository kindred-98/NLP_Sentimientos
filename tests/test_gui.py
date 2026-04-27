"""Tests para la interfaz grafica (GUI)."""

from __future__ import annotations

import tkinter as tk
from unittest.mock import patch

import pytest


class TestTema:
    """Tests para modulo tema."""

    def test_aplicar_tema_no_raises(self) -> None:
        from src.gui.tema import aplicar_tema

        style = tk.ttk.Style()
        aplicar_tema(style)

    def test_configurar_ventana_establece_geometria(self, root: tk.Tk) -> None:
        from src.gui.tema import configurar_ventana

        configurar_ventana(root)
        geo = root.geometry()
        assert "x" in geo
        assert "800" in geo

    def test_colores_definidos(self) -> None:
        from src.gui.tema import BG, FG, WHITE

        assert BG == "#dcdad5"
        assert FG == "black"
        assert WHITE == "white"

    def test_columnas_definidas(self) -> None:
        from src.gui.tema import COLUMNS, HIST_COLUMNS

        assert COLUMNS == ("nivel", "sentimiento", "polaridad", "intensidad")
        assert HIST_COLUMNS == ("fecha", "texto_resumido", "sentimiento")


class TestWidgets:
    """Tests para modulo widgets."""

    def test_widgets_se_crea_sin_error(self, root: tk.Tk) -> None:
        from src.gui.widgets import Widgets

        widgets = Widgets(root)
        assert widgets.txt_input is not None

    def test_construir_ventana_retorna_widgets(self, root: tk.Tk) -> None:
        from src.gui.widgets import construir_ventana

        w = construir_ventana(root)
        assert w.btn_analizar is not None
        assert w.btn_limpiar is not None
        assert w.btn_guardar is not None

    def test_widgets_tiene_tree(self, root: tk.Tk) -> None:
        from src.gui.widgets import Widgets

        w = Widgets(root)
        assert w.tree is not None
        assert w.tree_hist is not None

    def test_widgets_tiene_notebook(self, root: tk.Tk) -> None:
        from src.gui.widgets import Widgets

        w = Widgets(root)
        assert w.notebook is not None
        assert w.tab_tabla is not None
        assert w.tab_json is not None
        assert w.tab_just is not None
        assert w.tab_historial is not None


@pytest.fixture
def root() -> tk.Tk:
    """Crea una raiz de tkinter para testing."""
    root = tk.Tk()
    yield root
    try:
        root.destroy()
    except Exception:
        pass