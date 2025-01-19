from __future__ import annotations

import dataclasses
import importlib.resources
import json
import os.path

import qt_theme

try:
    from PySide6 import QtGui, QtWidgets
except ImportError:
    from PySide2 import QtGui, QtWidgets

ColorGroup = QtGui.QPalette.ColorGroup
ColorRole = QtGui.QPalette.ColorRole


@dataclasses.dataclass
class ColorScheme:
    primary: QtGui.QColor | None = None
    secondary: QtGui.QColor | None = None

    magenta: QtGui.QColor | None = None
    red: QtGui.QColor | None = None
    orange: QtGui.QColor | None = None
    yellow: QtGui.QColor | None = None
    green: QtGui.QColor | None = None
    cyan: QtGui.QColor | None = None
    blue: QtGui.QColor | None = None

    text: QtGui.QColor | None = None
    subtext1: QtGui.QColor | None = None
    subtext0: QtGui.QColor | None = None
    overlay2: QtGui.QColor | None = None
    overlay1: QtGui.QColor | None = None
    overlay0: QtGui.QColor | None = None
    surface2: QtGui.QColor | None = None
    surface1: QtGui.QColor | None = None
    surface0: QtGui.QColor | None = None
    base: QtGui.QColor | None = None
    mantle: QtGui.QColor | None = None
    crust: QtGui.QColor | None = None

    def is_dark_theme(self) -> bool:
        return self.text.value() > self.base.value()


def load_color_scheme(name: str) -> ColorScheme:
    """
    Returns the scheme with `name`.

    :raises ValueError: if scheme does not exist.
    """

    color_schemes_paths = [
        str(importlib.resources.files(qt_theme).joinpath('color_schemes')),
        os.getenv('QT_COLOR_SCHEMES'),
    ]

    file_name = f'{name}.json'
    for color_schemes_path in color_schemes_paths:
        if color_schemes_path:
            path = os.path.join(color_schemes_path, file_name)
            if os.path.exists(path):
                break
    else:
        raise ValueError(f'cannot find theme {file_name!r}')

    with open(str(path)) as f:
        data = json.load(f)

    colors = {key: QtGui.QColor(value) for key, value in data.items()}
    scheme = ColorScheme(**colors)
    return scheme


def set_palette_scheme(palette: QtGui.QPalette, scheme: ColorScheme):
    if scheme.primary.valueF() > 0.5:
        highlighted_text_color = scheme.mantle
    else:
        highlighted_text_color = scheme.text

    # base
    palette.setColor(ColorRole.Window, scheme.base)
    palette.setColor(ColorRole.WindowText, scheme.text)
    palette.setColor(ColorRole.Base, scheme.mantle)
    palette.setColor(ColorRole.AlternateBase, scheme.surface0)
    palette.setColor(ColorRole.ToolTipBase, scheme.mantle)
    palette.setColor(ColorRole.ToolTipText, scheme.text)
    palette.setColor(ColorRole.PlaceholderText, scheme.text)
    palette.setColor(ColorRole.Text, scheme.text)
    palette.setColor(ColorRole.Button, scheme.base)
    palette.setColor(ColorRole.ButtonText, scheme.text)
    palette.setColor(ColorRole.BrightText, _invert_value(scheme.text))

    palette.setColor(ColorRole.Highlight, scheme.primary)
    palette.setColor(ColorRole.HighlightedText, highlighted_text_color)

    palette.setColor(ColorRole.Link, scheme.primary.darker(125))
    palette.setColor(ColorRole.LinkVisited, scheme.primary.darker(125))

    # Auto generate: Light, MidLight, Mid, Dark, Shadow colors
    h, s, button_v, a = scheme.base.getHsvF()

    light_v = scheme.mantle.valueF()
    if scheme.is_dark_theme():
        # Shadow < Light < MidLight < Button < Mid < Dark < Text
        black_v = scheme.text.valueF()
    else:
        #  Text < Shadow < Dark < Mid < Button < MidLight < Light
        black_v = scheme.crust.valueF()

    mid_light = QtGui.QColor.fromHsvF(h, s, _lerp(button_v, light_v, 0.5), a)
    mid = QtGui.QColor.fromHsvF(h, s, _lerp(black_v, button_v, 0.65), a)
    dark = QtGui.QColor.fromHsvF(h, s, _lerp(black_v, button_v, 0.35), a)

    palette.setColor(ColorRole.Light, scheme.mantle)
    palette.setColor(ColorRole.Midlight, mid_light)
    palette.setColor(ColorRole.Mid, mid)
    palette.setColor(ColorRole.Dark, dark)
    palette.setColor(ColorRole.Shadow, scheme.crust)

    # disabled
    palette.setColor(ColorGroup.Disabled, ColorRole.WindowText, dark)
    palette.setColor(ColorGroup.Disabled, ColorRole.Base, scheme.base)
    palette.setColor(ColorGroup.Disabled, ColorRole.AlternateBase, scheme.base)

    palette.setColor(ColorGroup.Disabled, ColorRole.PlaceholderText, dark)
    palette.setColor(ColorGroup.Disabled, ColorRole.Text, dark)
    palette.setColor(ColorGroup.Disabled, ColorRole.Button, scheme.surface0)
    palette.setColor(ColorGroup.Disabled, ColorRole.ButtonText, dark)
    palette.setColor(ColorGroup.Disabled, ColorRole.BrightText, scheme.mantle)

    palette.setColor(ColorGroup.Disabled, ColorRole.Highlight, scheme.base)
    palette.setColor(ColorGroup.Disabled, ColorRole.HighlightedText, scheme.surface0)

    palette.setColor(ColorGroup.Disabled, ColorRole.Link, dark)
    palette.setColor(ColorGroup.Disabled, ColorRole.LinkVisited, dark)


def set_color_scheme(color_scheme: ColorScheme | str) -> None:
    app = QtWidgets.QApplication.instance()
    if not app or not isinstance(app, QtWidgets.QApplication):
        raise RuntimeError('must construct QApplication before applying theme')

    palette = app.palette()
    if isinstance(color_scheme, str):
        color_scheme = load_color_scheme(color_scheme)
    set_palette_scheme(palette, color_scheme)
    app.setPalette(palette)

    if color_scheme.is_dark_theme():
        # QAbstractItemView alternating row color fix
        item_view_palette = QtGui.QPalette(palette)
        item_view_palette.setColor(
            ColorRole.AlternateBase, palette.color(ColorRole.Window)
        )
        app.setPalette(item_view_palette, QtWidgets.QAbstractItemView.__name__)  # noqa


def set_style(style: str) -> None:
    app = QtWidgets.QApplication.instance()
    if isinstance(app, QtWidgets.QApplication):
        app.setStyle(style)


def _invert_value(color: QtGui.QColor) -> QtGui.QColor:
    h, s, v, a = color.getHsvF()
    color = QtGui.QColor.fromHsvF(h, s, 1 - v, a)
    return color


def _lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b
