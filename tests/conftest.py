import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtWidgets import QApplication


@pytest.fixture(autouse=True)
def close_qt_windows() -> None:
    yield

    app = QApplication.instance()
    if app is None:
        return

    for widget in app.topLevelWidgets():
        widget.close()
        widget.deleteLater()

    app.processEvents()
