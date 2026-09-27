from __future__ import annotations

import dataclasses

from PySide6 import QtGui, QtWidgets

import qt_themes
from qt_themes import Theme

ColorRole = QtGui.QPalette.ColorRole

BUNDLED_THEMES = {
    'atom_one',
    'blender',
    'catppuccin_frappe',
    'catppuccin_latte',
    'catppuccin_macchiato',
    'catppuccin_mocha',
    'dracula',
    'github_dark',
    'github_light',
    'modern_dark',
    'modern_light',
    'monokai',
    'nord',
    'one_dark_two',
}

COLORS = tuple(field.name for field in dataclasses.fields(Theme))


def get(name: str) -> Theme:
    theme = qt_themes.get_theme(name)
    assert theme is not None
    return theme


def test_get_themes() -> None:
    themes = qt_themes.get_themes()

    assert BUNDLED_THEMES.issubset(themes)
    for theme in themes.values():
        for color in COLORS:
            value = getattr(theme, color)
            assert isinstance(value, QtGui.QColor)
            assert value.isValid()


def test_get_theme() -> None:
    assert qt_themes.get_theme('nord') == qt_themes.get_themes()['nord']
    assert qt_themes.get_theme('missing') is None


def test_is_dark_theme() -> None:
    assert get('catppuccin_mocha').is_dark_theme()
    assert not get('catppuccin_latte').is_dark_theme()


def test_update_palette() -> None:
    theme = get('nord')
    palette = QtGui.QPalette()
    qt_themes.update_palette(palette, theme)

    assert palette.color(ColorRole.Window) == theme.base
    assert palette.color(ColorRole.Text) == theme.text
    assert palette.color(ColorRole.Highlight) == theme.primary
    assert palette.color(ColorRole.HighlightedText) == theme.mantle
    assert palette.color(ColorRole.Link) == theme.secondary


def test_set_theme(app: QtWidgets.QApplication) -> None:
    theme = get('nord')
    qt_themes.set_theme('nord', style=None)

    assert app.palette().color(ColorRole.Window) == theme.base
    assert app.property('theme') == theme
    assert qt_themes.get_theme() == theme

    qt_themes.set_theme(None, style=None)
    assert qt_themes.get_theme() is None


def test_set_widget_theme(app: QtWidgets.QApplication) -> None:
    theme = get('dracula')
    widget = QtWidgets.QWidget()
    qt_themes.set_widget_theme(widget, 'dracula', style=None)

    assert widget.palette().color(ColorRole.Window) == theme.base
    assert widget.property('theme') == theme

    qt_themes.set_widget_theme(widget, None, style=None)
    assert widget.property('theme') is None
