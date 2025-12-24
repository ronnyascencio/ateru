# xolo_core/ui/xolo_window.py

import os
from pathlib import Path
from typing import Any, Optional

from PySide6 import QtWidgets
from PySide6.QtGui import QStandardItem, QStandardItemModel

from core.xolo_core.generators.version_generator import VersionManager
from core.xolo_core.ui.xolo_ui import XoloUI
from core.xolo_core.utils.logging import log_core


class XoloMainWindow(QtWidgets.QMainWindow):
    def __init__(self, dcc: str, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        # --- Atributos de Datos ---
        self.dcc: str = dcc.lower()
        self.current_folder: Optional[Path] = (
            None  # Definido como Optional para Pyright
        )
        self.files: list[Any] = []

        log_core(f"DCC:{self.dcc}")

        # --- Window Setup ---
        self.setWindowTitle("Xolo Pipeline Saver")
        self.resize(600, 300)

        # --- UI Setup ---
        self.ui_wrapper = XoloUI(self)
        # 'self.controls' marcado como Any mata los errores de "Attribute unknown"
        self.controls: Any = self.ui_wrapper.ui
        self.setCentralWidget(self.ui_wrapper)

        # --- Internal models ---
        self.shots_model = QStandardItemModel()
        self.scenes_model = QStandardItemModel()

        # --- Inicialización ---
        self._connect_signals()
        self._set_project_name()
        self._load_shots()

        # Página por defecto
        self.controls.stackedWidget.setCurrentWidget(self.controls.saver_page)

    def _connect_signals(self):
        """Conecta las señales usando el alias 'controls'"""
        self.controls.saver_btn.clicked.connect(self.show_saver_page)
        self.controls.opener_btn.clicked.connect(self.show_opener_page)
        self.controls.shots_opener_lv.clicked.connect(self.on_shot_clicked)

    # --- Slots ---
    def show_saver_page(self):
        self.controls.stackedWidget.setCurrentWidget(self.controls.saver_page)

    def show_opener_page(self):
        self.controls.stackedWidget.setCurrentWidget(self.controls.opener_page)

    def refresh_file_list(self):
        """Refresca la lista de archivos validando el tipo Path"""
        # Limpiar lista (asumiendo que list_files es un widget de la UI)
        if hasattr(self.controls, "list_files"):
            self.controls.list_files.clear()

        # Validación de tipo para evitar: "Path | None is not assignable to Path"
        if self.current_folder is not None:
            # Aquí Pyright ya sabe que current_folder es Path
            # self.files = find_images_in_dir(self.current_folder)
            pass
        else:
            self.files = []

    # --- Helpers Core ---
    def _set_project_name(self):
        project_root = os.getenv("PROJECT_ROOT")

        if not project_root:
            self.controls.project_name_lbl.setText("No Project")
            return

        # Obtener el nombre de la carpeta raíz
        project_name = project_root.rstrip("/").split("/")[-1]
        self.controls.project_name_lbl.setText(project_name)

    def _load_shots(self):
        """Populate shots in both saver & opener views"""
        self.shots_model.clear()

        project_root = os.getenv("PROJECT_ROOT")
        if not project_root:
            return

        shots = VersionManager.get_shots(project_root)

        for shot in shots:
            item = QStandardItem(str(shot))
            item.setEditable(False)
            self.shots_model.appendRow(item)

        self.controls.shots_saver_lv.setModel(self.shots_model)
        self.controls.shots_opener_lv.setModel(self.shots_model)

    def on_shot_clicked(self, index):
        """Triggered when a shot is clicked"""
        shot_name = index.data()
        print(f"[XOLO] Shot selected: {shot_name}")
        self._load_scenes(shot_name)

    def _load_scenes(self, shot_name: str):
        """Populate scenes based on selected shot"""
        self.scenes_model.clear()

        project_root = os.getenv("PROJECT_ROOT")
        if not project_root:
            return

        scenes = VersionManager.get_work_shot_version(
            project_root=project_root, shot=shot_name, dcc=self.dcc
        )

        for scene in scenes:
            item = QStandardItem(str(scene))
            item.setEditable(False)
            self.scenes_model.appendRow(item)

        self.controls.scences_opener_lv.setModel(self.scenes_model)
