import contextlib
import sys

from PySide6 import QtGui, QtWidgets

from qt_theme import set_color_scheme

ColorGroup = QtGui.QPalette.ColorGroup
ColorRole = QtGui.QPalette.ColorRole

ROLES = (
    ColorRole.Window,
    ColorRole.WindowText,
    ColorRole.Base,
    ColorRole.AlternateBase,
    ColorRole.ToolTipBase,
    ColorRole.ToolTipText,
    ColorRole.PlaceholderText,
    ColorRole.Text,
    ColorRole.Button,
    ColorRole.ButtonText,
    ColorRole.BrightText,
    ColorRole.Highlight,
    ColorRole.HighlightedText,
    ColorRole.Link,
    ColorRole.LinkVisited,
    ColorRole.Accent,
    ColorRole.Light,
    ColorRole.Midlight,
    ColorRole.Mid,
    ColorRole.Dark,
    ColorRole.Shadow,
)

TEXT_ROLES = (
    ColorRole.WindowText,
    ColorRole.ToolTipText,
    ColorRole.Text,
    ColorRole.ButtonText,
    ColorRole.BrightText,
    ColorRole.HighlightedText,
    ColorRole.Light,
)


@contextlib.contextmanager
def application() -> QtWidgets.QApplication:
    if app := QtWidgets.QApplication.instance():
        yield app
        return

    app = QtWidgets.QApplication(sys.argv)
    yield app
    app.exec_()


def test_color_roles() -> None:
    with application():
        set_color_scheme('monokai')

        widget = QtWidgets.QWidget()
        widget.setMinimumWidth(400)
        main_layout = QtWidgets.QVBoxLayout()
        widget.setLayout(main_layout)

        for role in ROLES:
            layout = QtWidgets.QHBoxLayout()
            main_layout.addLayout(layout)
            for enabled in (True, False):
                # frame
                frame = QtWidgets.QFrame()
                frame.setEnabled(enabled)
                frame.setBackgroundRole(role)

                frame.setAutoFillBackground(True)
                frame.setLayout(QtWidgets.QHBoxLayout())
                layout.addWidget(frame)

                # label
                palette = frame.palette()
                background_color = palette.color(role)

                rgb = background_color.getRgbF()[:3]
                rgb_text = ', '.join(f'{v:.2f}' for v in rgb)
                label = QtWidgets.QLabel(f'({rgb_text}) {role}')

                if background_color.valueF() > 0.5:
                    text_color = QtGui.QColorConstants.Black
                else:
                    text_color = QtGui.QColorConstants.White
                for text_role in TEXT_ROLES:
                    palette.setColor(text_role, text_color)
                label.setPalette(palette)
                frame.layout().addWidget(label)

        widget.show()


if __name__ == '__main__':
    test_color_roles()
