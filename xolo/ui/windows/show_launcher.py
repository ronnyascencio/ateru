import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QObject, Qt
from PySide6.QtGui import QColor, QBrush

from xolo.core.logging import events
from xolo.core.config.utility import user_name
from xolo.core.api import (
    create_project,
    delete_project,
    scan_projects,
    project_data,
    update_project_status,
)
from xolo.ui.bar import ProgressController


class XoloLauncher(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_path = Path(__file__).parent.parent / "uix" / "launcher.ui"
        ui_file = QFile(str(ui_path))
        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"Cannot open UI file {ui_path}")
        self._ui = loader.load(ui_file)
        ui_file.close()
        if not self._ui:
            raise RuntimeError("UI could not be loaded")

        self.setCentralWidget(self._ui)
        self.resize(self._ui.size())
        self.setWindowTitle("Xolo Launcher")

        """ Connections """
        self.ui("launcher_projects_comboBox").addItems(self.projects_listed())

    """ UI helpers start"""

    def ui(self, name):
        w = self._ui.findChild(QObject, name)
        if not w:
            raise RuntimeError(f"UI widget not found: {name}")
        return w

    """ UI helpers ends"""

    """ Actions """

    ### projects
    #
    def projects_listed(self) -> list[str]:
        return sorted(scan_projects())

    """ Close """

    def closeEvent(self, event):
        events.success("[UI] process finished of Xolo launcher...")
        event.accept()
        QApplication.quit()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    window = XoloLauncher()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
