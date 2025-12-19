# tools/test_ui.py

from PySide6.QtWidgets import QApplication
from core.xolo_core.ui.xolo_window import XoloMainWindow

app = QApplication([])
win = XoloMainWindow()
win.show()
app.exec()
