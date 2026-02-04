# xolo/ui/windows/show_asset_manager.py
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QObject

from xolo.core.logging import events
from xolo.core.api_runtime import XoloRuntime


class XoloAssetManager(QMainWindow):
    def __init__(self):
        super().__init__()

        # ---------------- UI ----------------
        loader = QUiLoader()
        ui_path = Path(__file__).parent.parent / "uix" / "asset_manager.ui"
        ui_file = QFile(str(ui_path))

        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"Cannot open UI file {ui_path}")

        self._ui = loader.load(ui_file)
        ui_file.close()

        if not self._ui:
            raise RuntimeError("UI could not be loaded")

        self.setCentralWidget(self._ui)
        self.resize(self._ui.size())
        self.setWindowTitle("Xolo Asset Manager")

        # ---------------- Runtime ----------------
        self.runtime = XoloRuntime()
        self.runtime.initialize()  # fire

        # ---------------- Buttons ----------------
        self.ui("scene_open_pushButton").clicked.connect(self.open_scene)
        self.ui("scene_save_pushButton").clicked.connect(self.save_scene)

    # ---------------- UI Helper ----------------
    def ui(self, name):
        w = self._ui.findChild(QObject, name)
        if not w:
            raise RuntimeError(f"UI widget not found: {name}")
        return w

    # ---------------- Actions ----------------
    def open_scene(self):
        try:
            self.runtime.open_scene()
            events.success("Scene opened")
        except Exception as e:
            events.error(str(e))

    def save_scene(self):
        try:
            self.runtime.save_scene()
            events.success("Scene saved")
        except Exception as e:
            events.error(str(e))


def main():
    app = QApplication(sys.argv)
    window = XoloAssetManager()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
