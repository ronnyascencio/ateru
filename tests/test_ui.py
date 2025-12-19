# tests/test_ui.py
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_qt(monkeypatch):
    mock_app = MagicMock()
    monkeypatch.setattr("PySide6.QtWidgets.QApplication", lambda *args, **kwargs: mock_app)
    return mock_app

def test_xolo_main_window_can_instantiate(mock_qt):
    from core.xolo_core.ui.xolo_window import XoloMainWindow
    win = XoloMainWindow()
    assert win is not None
