from __future__ import annotations

import contextlib
import sys
from collections.abc import Iterator

from PySide6 import QtWidgets


@contextlib.contextmanager
def application() -> Iterator[QtWidgets.QApplication]:
    app = QtWidgets.QApplication.instance()
    if isinstance(app, QtWidgets.QApplication):
        yield app
        return

    app = QtWidgets.QApplication(sys.argv)
    yield app
    app.exec()
