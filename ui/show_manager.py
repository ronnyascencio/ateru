import sys
import os
from core.xolo_core.logging import events
from pathlib import Path


from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QObject


from core.xolo_core.api import create_project, delete_project, scan_projects


class XoloManager(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "uix" / "manager.ui"
        ui_file = QFile(str(ui_path))

        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"cant open the ui {ui_path}")

        self._ui = loader.load(ui_file)
        ui_file.close()

        if not self._ui:
            raise RuntimeError("Error UI not loaded")

        self.setCentralWidget(self._ui)
        self.resize(self._ui.size())
        self.setWindowTitle("Xolo Pipeline Manager")

        """ Connections """
        self.ui("create_project_pushButton").clicked.connect(self.project_create)
        self.ui("projects_delete_comboBox").addItems(self.projects_listed())
        self.ui("delete_project_pushButton").clicked.connect(self.project_delete)

    def ui(self, name):
        w = self._ui.findChild(QObject, name)
        if not w:
            raise RuntimeError(f"UI widget not found: {name}")
        return w

    def project_create(self):
        project_name = self.ui("project_name_lineEdit").text()
        fps = self.ui("fps_lineEdit").text()
        res_str = self.ui("ress_lineEdit").text()

        try:
            width, height = map(int, res_str.lower().replace(" ", "").split("x"))
            create_project(
                project_name=project_name,
                fps=int(fps),
                width=str(width),
                height=str(height),
            )
            events.success(f"Project {project_name} done")
        except Exception as e:
            events.error(f"Error while creating project: {str(e)}")

    def projects_listed(self) -> list[str]:
        return sorted(scan_projects())

    def project_delete(self):
        project_name: str = self.ui("projects_delete_comboBox").currentText()
        try:
            delete_project(project_name)
            events.success(f"project: {project_name} deleted")
        except:
            events.error(f"project {project_name} could not be deleted")

    def closeEvent(self, event):
        events.success("[UI] Finalizando procesos de Xolo...")
        event.accept()
        QApplication.quit()


def main():
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(True)

    window = XoloManager()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
