from PySide6 import QtGui, QtWidgets, QtCore

import qt_themes
from tests import application

ColorGroup = QtGui.QPalette.ColorGroup
ColorRole = QtGui.QPalette.ColorRole

ROLES = (
    ColorRole.Window,
    ColorRole.WindowText,
    ColorRole.Base,
    ColorRole.AlternateBase,
    ColorRole.Text,
    ColorRole.PlaceholderText,
    ColorRole.BrightText,
    ColorRole.Button,
    ColorRole.ButtonText,
    ColorRole.ToolTipBase,
    ColorRole.ToolTipText,
    ColorRole.Link,
    ColorRole.LinkVisited,
    ColorRole.Highlight,
    ColorRole.HighlightedText,
    ColorRole.Accent,
    ColorRole.Light,
    ColorRole.Midlight,
    ColorRole.Mid,
    ColorRole.Dark,
    ColorRole.Shadow,
)

GROUPS = (ColorGroup.Normal, ColorGroup.Inactive, ColorGroup.Disabled)


class ColorRoleWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self._init_ui()
        self._update_colors()

    def _init_ui(self) -> None:
        self.setWindowTitle('Color Roles')
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
        self.setMinimumWidth(800)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Theme Dropdown
        control_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(control_layout)
        theme_label = QtWidgets.QLabel('Theme:')
        control_layout.addWidget(theme_label)
        theme_combobox = QtWidgets.QComboBox()
        names = ['default']
        names.extend(qt_themes.get_themes().keys())
        theme_combobox.addItems(names)
        theme_combobox.currentTextChanged.connect(self._set_theme)
        control_layout.addWidget(theme_combobox)
        control_layout.addStretch()

        # Color Widget
        self.color_widget = None

    def _update_colors(self) -> None:
        if self.color_widget:
            self.color_widget.deleteLater()

        self.color_widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        self.color_widget.setLayout(layout)
        self.layout().addWidget(self.color_widget)

        # Color Roles
        app = QtWidgets.QApplication.instance()
        if not isinstance(app, QtWidgets.QApplication):
            return

        app_palette = app.palette()

        for i, group in enumerate(GROUPS):
            layout.addWidget(QtWidgets.QLabel(str(group)), 0, i + 1)

        for i, role in enumerate(ROLES):
            role_label = QtWidgets.QLabel(str(role))
            layout.addWidget(role_label, i + 1, 0)

            colors = []
            for j, group in enumerate(GROUPS):
                background_color = app_palette.color(group, role)
                if background_color.valueF() > 0.5:
                    text_color = QtGui.QColorConstants.Black
                else:
                    text_color = QtGui.QColorConstants.White
                colors.append(background_color)

                # frame
                frame = QtWidgets.QFrame()
                palette = frame.palette()
                palette.setColor(ColorRole.Window, background_color)
                palette.setColor(ColorRole.WindowText, text_color)
                frame.setPalette(palette)
                frame.setAutoFillBackground(True)

                frame.setLayout(QtWidgets.QHBoxLayout())
                layout.addWidget(frame, i + 1, j + 1)

                # label
                rgb = background_color.getRgbF()[:3]
                rgb_text = ', '.join(f'{v:.2f}' for v in rgb)
                label = QtWidgets.QLabel(f'({rgb_text})')
                frame.layout().addWidget(label)

            if all(color == colors[0] for color in colors):
                font = role_label.font()
                font.setBold(True)
                role_label.setFont(font)

    def _set_theme(self, theme: str) -> None:
        if theme == 'default':
            theme = None
        qt_themes.set_theme(theme)
        self._update_colors()


def test_color_roles() -> None:
    with application():
        widget = ColorRoleWidget()
        widget.show()


if __name__ == '__main__':
    test_color_roles()
