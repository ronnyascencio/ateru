import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QObject, Qt
from PySide6.QtGui import QColor, QBrush

from core.xolo_core.logging import events
from core.xolo_core.config.utility import user_name
from core.xolo_core.api import (
    create_project,
    delete_project,
    scan_projects,
    project_data,
    update_project_status,
)
from ui.bar import ProgressController


class XoloManager(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "uix" / "manager.ui"
        ui_file = QFile(str(ui_path))
        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"Cannot open UI file {ui_path}")
        self._ui = loader.load(ui_file)
        ui_file.close()
        if not self._ui:
            raise RuntimeError("UI could not be loaded")

        self.setCentralWidget(self._ui)
        self.resize(self._ui.size())
        self.setWindowTitle("Xolo Pipeline Manager")

        self.ui("status_progressBar").setVisible(False)

        self.progress = ProgressController(
            ui=self.ui,
            enable_fn=lambda: self.set_ui_enabled(True),
            disable_fn=lambda: self.set_ui_enabled(False),
            min_duration_ms=600,
        )

        """ Connections """

        self.ui("user_label").setText(user_name())
        self.ui("create_project_pushButton").clicked.connect(self.project_create)
        self.ui("delete_project_pushButton").clicked.connect(self.project_delete)
        self.ui("update_projects_pushButton").clicked.connect(self.refresh_projects)

        self.ui("projects_tableWidget").cellChanged.connect(self.on_table_cell_changed)

        self.refresh_projects()

    """ UI helpers start"""

    def ui(self, name):
        w = self._ui.findChild(QObject, name)
        if not w:
            raise RuntimeError(f"UI widget not found: {name}")
        return w

    def set_ui_enabled(self, enabled: bool):
        self.ui("create_project_pushButton").setEnabled(enabled)
        self.ui("delete_project_pushButton").setEnabled(enabled)
        self.ui("update_projects_pushButton").setEnabled(enabled)
        self.ui("projects_delete_comboBox").setEnabled(enabled)

    """ UI helpers ends"""

    def refresh_projects(self):
        """refresh combo and table"""
        combo = self.ui("projects_delete_comboBox")
        combo.clear()
        combo.addItems(sorted(scan_projects()))
        self.populate_projects_table()

    def projects_listed(self) -> list[str]:
        return sorted(scan_projects())

    def populate_projects_table(self):
        """Fill table and color status"""
        table = self.ui("projects_tableWidget")
        projects = self.projects_listed()

        table.blockSignals(True)

        table.clearContents()
        table.setRowCount(len(projects))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Name", "Type", "Status"])

        for row, project_name in enumerate(projects):
            try:
                project_info = project_data(project_name)

                name_item = QTableWidgetItem(project_info.name)
                type_item = QTableWidgetItem(project_info.type)
                status_item = QTableWidgetItem(project_info.status)

                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                status_lower = project_info.status.lower()
                if "active" in status_lower:
                    status_item.setBackground(QBrush(QColor("green")))
                elif "archived" in status_lower:
                    status_item.setBackground(QBrush(QColor("red")))
                elif "hold" in status_lower:
                    status_item.setBackground(QBrush(QColor("purple")))
                else:
                    status_item.setBackground(QBrush(QColor("white")))

                table.setItem(row, 0, name_item)
                table.setItem(row, 1, type_item)
                table.setItem(row, 2, status_item)

            except Exception as e:
                print(f"Error leyendo proyecto {project_name}: {e}")
                continue

        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        table.blockSignals(False)

    """ Actions """

    def project_create(self):
        project_name = self.ui("project_name_lineEdit").text()
        fps = self.ui("fps_lineEdit").text()
        res_str = self.ui("ress_lineEdit").text()
        type_ = self.ui("project_type_lineEdit").text()

        self.progress.start()
        try:
            width, height = map(int, res_str.lower().replace(" ", "").split("x"))
            create_project(
                project_name=project_name,
                fps=int(fps),
                width=str(width),
                height=str(height),
                type=type_,
            )
            events.success(f"Project {project_name} created")
            self.progress.stop(
                on_done=lambda: (self.reset_project_form(), self.refresh_projects())
            )
        except Exception as e:
            events.error(f"Error creating project: {e}")
            self.progress.stop()

    def project_delete(self):
        project_name = self.ui("projects_delete_comboBox").currentText()
        if not project_name:
            return
        self.progress.start()
        try:
            delete_project(project_name)
            events.success(f"Project {project_name} deleted")
            self.progress.stop(on_done=self.refresh_projects)
        except Exception as e:
            events.error(f"Error deleting project {project_name}: {e}")
            self.progress.stop()

    def reset_project_form(self):
        self.ui("project_name_lineEdit").clear()
        self.ui("fps_lineEdit").clear()
        self.ui("ress_lineEdit").clear()
        self.ui("project_type_lineEdit").clear()

    """ Editable Tables """

    def on_table_cell_changed(self, row, column):
        if column != 2:
            return

        table = self.ui("projects_tableWidget")
        project_name = table.item(row, 0).text()
        new_status = table.item(row, column).text().strip()

        if not new_status:
            return

        self.progress.start()
        try:
            update_project_status(project_name, new_status)
            events.success(f"Status of {project_name} updated to {new_status}")

            status_item = table.item(row, column)
            if "active" in new_status.lower():
                status_item.setBackground(QBrush(QColor("green")))
            elif "archived" in new_status.lower():
                status_item.setBackground(QBrush(QColor("red")))
            elif "hold" in new_status.lower():
                status_item.setBackground(QBrush(QColor("purple")))
            else:
                status_item.setBackground(QBrush(QColor("white")))

        except Exception as e:
            events.error(f"could not update status of  {project_name}: {e}")
        finally:
            self.progress.stop()

    """ Close """

    def closeEvent(self, event):
        events.success("[UI] finishing process of Xolo...")
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
