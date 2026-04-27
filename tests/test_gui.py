"""Tests para la interfaz grafica (GUI)."""

from __future__ import annotations



class TestTema:
    """Tests para modulo tema."""

    def test_colores_definidos(self) -> None:
        from gui.tema import BG, FG, WHITE

        assert BG == "#dcdad5"
        assert FG == "black"
        assert WHITE == "white"

    def test_columnas_definidas(self) -> None:
        from gui.tema import COLUMNS, HIST_COLUMNS

        assert COLUMNS == ("nivel", "sentimiento", "polaridad", "intensidad")
        assert HIST_COLUMNS == ("fecha", "texto_resumido", "sentimiento")

    def test_fuentes_definidas(self) -> None:
        from gui.tema import FONT_BASE, FONT_BOLD

        assert FONT_BASE == ("Tahoma", 8)
        assert FONT_BOLD == ("Tahoma", 8, "bold")

    def test_dimensiones_ventana_definidas(self) -> None:
        from gui.tema import WINDOW_W, WINDOW_H

        assert WINDOW_W == 800
        assert WINDOW_H == 700


class TestWidgets:
    """Tests para modulo widgets."""

    def test_construir_ventana_existe(self) -> None:
        from gui.widgets import construir_ventana

        assert callable(construir_ventana)

    def test_widgets_class_existe(self) -> None:
        from gui.widgets import Widgets

        assert callable(Widgets)


class TestTemaCompleto:
    """Tests adicionales para tema."""

    def test_tema_configurar_ventana(self) -> None:
        import gui.tema

        assert hasattr(gui.tema, "configurar_ventana")
        assert callable(gui.tema.configurar_ventana)

    def test_tema_tiene_todas_constantes(self) -> None:
        from gui.tema import (
            WINDOW_MIN_W,
            WINDOW_MIN_H,
            TEXT_HEIGHT,
            TREE_ROWS,
            TREE_HIST_ROWS,
            TREE_COL_W,
            TAG_FAVORABLE,
            TAG_DESFAVORABLE,
        )

        assert WINDOW_MIN_W == 770
        assert WINDOW_MIN_H == 600
        assert TEXT_HEIGHT == 4
        assert TREE_ROWS == 6
        assert TREE_HIST_ROWS == 8
        assert TREE_COL_W == 150
        assert TAG_FAVORABLE == "favorable"
        assert TAG_DESFAVORABLE == "desfavorable"

    def test_tema_colores_emociones(self) -> None:
        from gui.tema import FG_POSITIVO, FG_NEGATIVO, FG_NEUTRAL

        assert FG_POSITIVO == "#008000"
        assert FG_NEGATIVO == "#D00000"
        assert FG_NEUTRAL == "#808080"