from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor, QBrush
from typing import Any, List

from core.xolo_core.api import project_data


class ProjectsTableModel(QAbstractTableModel):
    headers = ["Name", "Type", "Status"]

    def __init__(self, projects: List[str], parent=None):
        super().__init__(parent)
        self._projects = projects

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._projects)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 3

    def _data(self, index: QModelIndex, role: int) -> Any:
        if not index.isValid():
            return None

        project = project_data(self._projects[index.row()])

        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if column == 0:
                return project.name
            if column == 1:
                return project.type
            if column == 2:
                return project.status

        if role == Qt.ItemDataRole.ForegroundRole and column == 2:
            status = project.status.lower()
            if "active" in status:
                return QBrush(QColor("green"))
            if "archived" in status:
                return QBrush(QColor("darkred"))
            if "hold" in status:
                return QBrush(QColor("purple"))

        return None

    def _flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

        # only Status editable
        if index.column() == 2:
            flags |= Qt.ItemFlag.ItemIsEditable

        return flags

    def setdata(self, index: QModelIndex, value: Any, role: int) -> bool:
        if role == Qt.ItemDataRole.EditRole and index.column() == 2:
            project_name = self._projects[index.row()]
            from core.xolo_core.api import update_project_status
            update_project_status(project_name, str(value))
            self.dataChanged.emit(index, index, [role])
            return True

        return False

    def headerdata(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int
    ) -> Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return self.headers[section]

        return None
