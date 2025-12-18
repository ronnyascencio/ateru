# xolo_core/ui/xolo_window.py

import os
from PySide6 import QtWidgets
from PySide6.QtGui import QStandardItemModel, QStandardItem
from core.xolo_core.ui.xolo_ui import XoloUI
from core.xolo_core.generators.version_generator import VersionManager
from core.xolo_core.utils.logging import log_core, log_ui, log_error

class XoloMainWindow(QtWidgets.QMainWindow):
    def __init__(self, dcc: str,  parent=None):
        super().__init__(parent)

        """dcc auto detect"""
        self.dcc = dcc.lower()
        log_core(f"DCC:{self.dcc}")

        """ Window Setup"""
        self.setWindowTitle("Xolo Pipeline Saver")
        self.resize(600, 300)


        self.ui = XoloUI(self)
        self.setCentralWidget(self.ui)

        """ Internal models """
        self.shots_model = QStandardItemModel()
        self.scenes_model = QStandardItemModel()

        """ Signals connect"""
        self._connect_signals()
        self._set_project_name()
        self._load_shots()

        """ Default page """
        self.ui.ui.stackedWidget.setCurrentWidget(
            self.ui.ui.saver_page
        )


    def _connect_signals(self):
        self.ui.ui.saver_btn.clicked.connect(self.show_saver_page)
        self.ui.ui.opener_btn.clicked.connect(self.show_opener_page)
        self.ui.ui.shots_opener_lv.clicked.connect(
            self.on_shot_clicked
        )

    """ slots """
    def show_saver_page(self):
        self.ui.ui.stackedWidget.setCurrentWidget(
            self.ui.ui.saver_page
        )

    def show_opener_page(self):
        self.ui.ui.stackedWidget.setCurrentWidget(
            self.ui.ui.opener_page
        )

    """ helpers core"""
    def _set_project_name(self):
        project_root = os.getenv("PROJECT_ROOT")

        if not project_root:
            self.ui.ui.project_name_lbl.setText("No Project")
            return

        project_name = project_root.rstrip("/").split("/")[-1]
        self.ui.ui.project_name_lbl.setText(project_name)

    def _load_shots(self):
        """Populate shots in both saver & opener views"""
        self.shots_model.clear()

        project_root = os.getenv("PROJECT_ROOT")
        if not project_root:
            return

        shots = VersionManager.get_shots(project_root)

        for shot in shots:
            item = QStandardItem(shot)
            item.setEditable(False)
            self.shots_model.appendRow(item)

        self.ui.ui.shots_saver_lv.setModel(self.shots_model)
        self.ui.ui.shots_opener_lv.setModel(self.shots_model)

    def on_shot_clicked(self, index):
        """Triggered when a shot is clicked"""
        shot_name = index.data()
        print(f"[XOLO] Shot selected: {shot_name}")

        self._load_scenes(shot_name)

    def _load_scenes(self, shot_name):
        """Populate scenes based on selected shot"""
        self.scenes_model.clear()

        project_root = os.getenv("PROJECT_ROOT")
        if not project_root:
            return

        scenes = VersionManager.get_work_shot_version(project_root=project_root, shot=shot_name, dcc=self.dcc)

        for scene in scenes:
            item = QStandardItem(scene)
            item.setEditable(False)
            self.scenes_model.appendRow(item)



        self.ui.ui.scences_opener_lv.setModel(self.scenes_model)
