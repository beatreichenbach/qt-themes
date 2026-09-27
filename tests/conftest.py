from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
from PySide6 import QtWidgets


@pytest.fixture(scope='session')
def app() -> Iterator[QtWidgets.QApplication]:
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    app = QtWidgets.QApplication.instance()
    if not isinstance(app, QtWidgets.QApplication):
        app = QtWidgets.QApplication([])
    yield app
