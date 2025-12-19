# tools/test_ui.py

import os
import sys
import pytest

from PySide6.QtWidgets import QApplication

# Import lazy (importante)
@pytest.fixture(scope="session")
def qapp():
    """
    Ensure a QApplication exists.
    Does NOT start event loop.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_xolo_main_window_instantiates(qapp):
    """
    UI smoke test:
    - Can import window
    - Can instantiate it
    - No rendering / no exec
    """
    from core.xolo_core.ui.xolo_window import XoloMainWindow

    win = XoloMainWindow()

    assert win is not None
    assert win.windowTitle() != ""
