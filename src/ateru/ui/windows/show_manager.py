import sys
from pathlib import Path
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QObject, Qt
from PySide6.QtGui import QColor, QBrush

from ateru.core.logging import events
from ateru.core.config.utility import user_name
from ateru.core.api import (
    create_project,
    delete_project,
    scan_projects,
    project_data,
    count_shots,
    update_project_status,
    create_shot,
    scan_shots,
    scan_assets,
)
from ateru.ui.bar import ProgressController


class AteruManager(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_path = Path(__file__).parent.parent / "uix" / "manager.ui"
        ui_file = QFile(str(ui_path))
        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"Cannot open UI file {ui_path}")
        self._ui = loader.load(ui_file)
        ui_file.close()
        if not self._ui:
            raise RuntimeError("UI could not be loaded")

        self.setCentralWidget(self._ui)
        self.resize(self._ui.size())
        self.setWindowTitle("Ateru Pipeline Manager")

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
        self.ui("launcher_toolButton").clicked.connect(self.start_launcher)
        self.ui("settings_toolButton").clicked.connect(self.start_settings)

        self.ui("projects_tableWidget").cellChanged.connect(self.on_table_cell_changed)

        """ project tab"""
        self.ui("projects_tableWidget").itemSelectionChanged.connect(self.project_info)

        """ shots tab """
        self.ui("shots_project_comboBox").currentTextChanged.connect(self.refresh_shots)
        self.ui("shots_project_comboBox").addItems(self.projects_listed())
        self.ui("shot_create_pushButton").clicked.connect(self.shot_create)

        """ assets tab"""
        self.ui("assets_projects_comboBox").addItems(self.projects_listed())

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

    """ projects start"""

    def clear_project_info(self):
        self.ui("project_info_name_label").setText("-")
        self.ui("fps_project_info_label").setText("-")
        self.ui("resolution_project_info_label").setText("-")
        self.ui("shot_project_count_info_label").setText("0")

    def refresh_projects(self):
        projects = self.projects_listed()

        combo = self.ui("projects_delete_comboBox")
        combo.clear()
        combo.addItems(projects)

        shots_combo = self.ui("shots_project_comboBox")
        shots_combo.clear()
        shots_combo.addItems(projects)

        self.populate_projects_table()
        self.populate_shots_table()

    def projects_listed(self) -> list[str]:
        return sorted(scan_projects())

    def populate_projects_table(self):
        table = self.ui("projects_tableWidget")
        projects = self.projects_listed()

        table.blockSignals(True)
        table.clearContents()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Name", "Type", "Status"])

        if not projects:
            table.setRowCount(0)
            table.blockSignals(False)
            self.clear_project_info()
            return

        table.setRowCount(len(projects))

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
                    status_item.setForeground(QBrush(QColor("green")))
                elif "archived" in status_lower:
                    status_item.setForeground(QBrush(QColor("darkRed")))
                elif "hold" in status_lower:
                    status_item.setForeground(QBrush(QColor("purple")))
                else:
                    status_item.setForeground(QBrush(QColor("white")))

                table.setItem(row, 0, name_item)
                table.setItem(row, 1, type_item)
                table.setItem(row, 2, status_item)

            except Exception as e:
                print(f"Error leyendo proyecto {project_name}: {e}")

        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        table.blockSignals(False)

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

    """ info project start """

    def project_info(self):
        table = self.ui("projects_tableWidget")

        row = table.currentRow()
        if row == -1:
            return  # nada seleccionado

        item = table.item(row, 0)  # columna 0 = name
        if item is None:
            return

        project_name = item.text()
        project = project_data(project_name)
        name = project.name
        fps = project.fps
        separator = "x"
        resolution = separator.join(project.resolution)
        shots_number = str(count_shots(project.name))

        self.ui("project_info_name_label").setText(name)
        self.ui("fps_project_info_label").setText(str(fps))
        self.ui("resolution_project_info_label").setText(resolution)
        self.ui("shot_project_count_info_label").setText(str(shots_number))

    """ info project ends """

    """ projects ends"""

    """ shots tab start """

    def selected_shots_project(self) -> str | None:
        combo = self.ui("shots_project_comboBox")
        project = combo.currentText().strip()
        return project if project else None

    def shots_listed(self):
        project_name = self.ui("shots_project_comboBox").currentText()
        shots = scan_shots(project_name)

        return shots

    def populate_shots_table(self):
        table = self.ui("shots_manager_tableWidget")
        project_name = self.selected_shots_project()

        table.blockSignals(True)
        table.clearContents()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Name", "Status", "Deadline", "Priority"])

        if not project_name:
            table.setRowCount(0)
            table.blockSignals(False)
            return

        shots = scan_shots(project_name)

        if not shots:
            table.setRowCount(0)
            table.blockSignals(False)
            return

        table.setRowCount(len(shots))

        for row, shot_name in enumerate(shots):
            table.setItem(row, 0, QTableWidgetItem(shot_name))
            table.setItem(row, 1, QTableWidgetItem("WIP"))
            table.setItem(row, 2, QTableWidgetItem("-"))
            table.setItem(row, 3, QTableWidgetItem("Normal"))

            for col in range(table.columnCount()):
                item = table.item(row, col)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        table.blockSignals(False)

    def refresh_shots(self):
        self.populate_shots_table()

    def shot_create(self):
        project = self.ui("shots_project_comboBox").currentText().strip()
        shot_name = self.ui("name_shot_lineEdit").text()
        start = self.ui("start_shots_lineEdit").text()
        end = self.ui("end_shots_lineEdit").text()
        fps = self.ui("fps_shots_lineEdit").text()
        priority = self.ui("priority_shots_comboBox").currentText()

        self.progress.start()

        create_shot(
            project_name=project,
            shot_name=shot_name,
            start=start,
            end=end,
            fps=fps,
            priority=priority,
        )
        self.populate_shots_table()
        self.progress.stop(
            on_done=lambda: (self.reset_shots_form(), self.refresh_shots())
        )

    def reset_shots_form(self):
        self.ui("name_shot_lineEdit").clear()
        self.ui("start_shots_lineEdit").clear()
        self.ui("end_shots_lineEdit").clear()
        self.ui("fps_shots_lineEdit").clear()

    """ shots tab ends"""

    """ assets tab start"""

    """ assets tab ends"""

    """ launcher start"""

    def start_launcher(self):
        process = subprocess.Popen(
            [sys.executable, "src/ateru/ui/windows/show_launcher.py"],
            stdout=None,
            stderr=None,
        )

        try:
            process.wait()

        except KeyboardInterrupt:
            process.terminate()

    """ launcher ends"""

    """ start settings"""

    def start_settings(self):
        process = subprocess.Popen(
            [sys.executable, "src/ateru/ui/windows/show_settings.py"],
            stdout=None,
            stderr=None,
        )

    """ ends settings"""

    """ Close """

    def closeEvent(self, event):
        events.success("[UI] process finished of Ateru Manager...")
        event.accept()
        QApplication.quit()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    window = AteruManager()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
