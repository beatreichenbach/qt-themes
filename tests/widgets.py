from PySide6 import QtWidgets
import qt_theme


def test_widgets() -> None:
    app = QtWidgets.QApplication()
    qt_theme.set_color_scheme('nord')
    widget = QtWidgets.QWidget()
    widget.setLayout(QtWidgets.QVBoxLayout())

    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(QtWidgets.QLabel('Label'))

    combo_box = QtWidgets.QComboBox()
    combo_box.addItem('Item')
    layout.addWidget(combo_box)

    combo_box = QtWidgets.QCheckBox()
    combo_box.addItem('Item')
    layout.addWidget(combo_box)

    widget.show()
    app.exec()
