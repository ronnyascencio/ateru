# xolo_core/ui/xolo_window.py

from PySide6 import QtWidgets
from core.xolo_core.ui.xolo_ui import XoloUI


class XoloMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Xolo Pipeline")

        self.ui = XoloUI(self)
        self.setCentralWidget(self.ui)

        self.resize(600, 300)
