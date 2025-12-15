# xolo_core/ui/xolo_ui.py

from pathlib import Path
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader


UI_PATH = Path(__file__).parent / "xolo.ui"


class XoloUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        loader = QUiLoader()
        self.ui = loader.load(str(UI_PATH), self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)
