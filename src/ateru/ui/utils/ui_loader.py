from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget
from pathlib import Path


def load_ui(ui_path: str, parent: QWidget) -> QWidget:
    """
    Carga un archivo .ui y devuelve el QWidget correspondiente.
    """
    ui_file = Path(ui_path)
    if not ui_file.exists():
        raise FileNotFoundError(f"UI file not found: {ui_file}")

    loader = QUiLoader()
    widget = loader.load(str(ui_file), parent)
    if widget is None:
        raise RuntimeError(f"Failed to load UI: {ui_file}")
    return widget
