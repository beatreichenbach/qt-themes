import contextlib
import sys

from PySide6 import QtWidgets


@contextlib.contextmanager
def application() -> QtWidgets.QApplication:
    if app := QtWidgets.QApplication.instance():
        yield app
        return

    app = QtWidgets.QApplication(sys.argv)
    yield app
    app.exec()
