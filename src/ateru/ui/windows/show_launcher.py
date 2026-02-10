import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QObject, Qt
from PySide6.QtGui import QColor, QBrush, QIcon
from ateru.ui.uix import ateru_rc
from ateru.core.logging import events
from ateru.core.config.utility import user_name
from ateru.core.api import (
    create_project,
    delete_project,
    scan_projects,
    project_data,
    update_project_status,
    merge_pythonpath,
)
from ateru.core.config import loader
from ateru.core.launcher import launch

# from ateru.core.api_runtime import AteruRuntime
from ateru.ui.bar import ProgressController


class AteruLauncher(QMainWindow):
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

        # self.dcc = AteruRuntime()
        # self.dcc.initialize()

        self.setWindowIcon(QIcon(":/manager/icons/ateru.svg"))

        self.setCentralWidget(self._ui)
        self.resize(self._ui.size())
        self.setWindowTitle("Ateru Launcher")

        """ Connections """
        self.ui("launcher_projects_comboBox").addItems(self.projects_listed())
        self.ui("nuke_pushButton").clicked.connect(self.nuke_launch)

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

    """ nuke launch start """

    def nuke_launch(self):
        dcc_str: str = "nuke"
        executable = str(loader.read_ateru_config_apps(dcc_str))
        launch(dcc=dcc_str, executable=executable)

    """ nuke launch ends """

    """ Close """

    def closeEvent(self, event):
        events.success("[UI] process finished of Ateru launcher...")
        event.accept()
        QApplication.quit()




def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    window = AteruLauncher()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

