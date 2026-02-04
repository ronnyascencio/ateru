import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QObject

from core.xolo_core.logging import events
from core.xolo_core.api import set_software_paths, set_projects_root


class XoloSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "uix" / "settings.ui"

        ui_file = QFile(str(ui_path))
        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"Cannot open UI file {ui_path}")

        self._ui = loader.load(ui_file)
        ui_file.close()

        if not self._ui:
            raise RuntimeError("UI could not be loaded")

        # ---------- Attach layout safely ----------
        layout = self._ui.layout()
        if layout is None:
            raise RuntimeError(
                "The .ui file has no root layout. "
                "Add a layout to the top-level widget in Qt Designer."
            )

        self.setLayout(layout)

        # ---------- Window setup ----------
        self.setWindowTitle("Xolo Settings")
        self.resize(self._ui.size())
        self.setModal(True)

        # ---------- Connections ----------
        self.ui("project_path_set_pushButton").clicked.connect(self.set_projects_path)
        self.ui("software_set_pushButton").clicked.connect(self.set_softwares_paths)

    # ---------- UI helpers ----------
    def ui(self, name: str):
        widget = self.findChild(QObject, name)
        if not widget:
            raise RuntimeError(f"UI widget not found: {name}")
        return widget

    # -------------------------------

    def closeEvent(self, event):
        event.accept()

    def set_projects_path(self):
        projects_path = self.ui("projects_global_path_lineEdit").text()
        ocio_path = self.ui("ocio_path_lineEdit").text()

        set_projects_root(root=projects_path, ocio=ocio_path)
        events.success("roots global config set")

    def set_softwares_paths(self):
        nuke_path = self.ui("nuke_path_lineEdit").text()
        gaffer_path = self.ui("gaffer_path_lineEdit").text()
        blender_path = self.ui("blender_path_lineEdit").text()
        set_software_paths(nuke=nuke_path, gaffer=gaffer_path, blender=blender_path)
        events.success("software global config set")


def main():
    app = QApplication(sys.argv)
    dialog = XoloSettings()
    dialog.exec()
    sys.exit(0)


if __name__ == "__main__":
    main()
