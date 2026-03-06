
from PySide6.QtWidgets import QWidget
from ateru.ui.utils.ui_loader import load_ui
from pathlib import Path

class NukeTools(QWidget):
    """Widget para la sección Tools de Nuke."""
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = Path(__file__).parent.parent.parent / "uix" / "nuke" / "nuke_tools.ui"
        self.ui = load_ui(ui_path, parent=self)
