import os
import re
from pathlib import Path
from core.xolo_core.extractors.dcc import load_map
from core.xolo_core.utils.logging import log_core, log_error
"""Global Variables"""



class VersionManager:
    ASSETS_DIR = os.environ.get("ASSETS_ROOT")

    @staticmethod
    def get_shots(path: str):
        """return a list of shots available in the shots directory"""
        shots_dir = Path(path) / "shots"
        shots = []
        if not shots_dir.exists() or not shots_dir.is_dir():
            return shots
        else:
            for shot in os.listdir(shots_dir):
                shots.append(shot)

        return sorted(shots)

    @staticmethod
    def get_work_shot_version(project_root: str, shot: str, dcc: str):
        """returns list of versions available for a given shot"""

        try:
            extensions = load_map(dcc)  # 👈 lista de extensiones
        except Exception as e:
            log_error(f"error in extensions loader {e}")
            return []


        versions_dir = Path(str(project_root)) / "shots" / shot / "work" / dcc
        debug_print = Path() / "PROJECT_ROOT" / "shots" / shot / "work" / dcc

        log_core(f"PROJECT_ROOT variable path : {project_root}")
        log_core(f"Looking for scenes in: {debug_print}")

        if not versions_dir.exists():
            return []

        scenes = []

        for file_path in versions_dir.iterdir():
            if file_path.is_file() and file_path.suffix in extensions:
                scenes.append(file_path.name)

        return sorted(scenes)


    @staticmethod
    def get_work_asset_version(department: str, asset_name: str):
        """returns list of assets available in the assets directory"""

        asset_work_dir = Path(str(ASSETS_DIR)) / "work"
        assets = []
        return print(asset_work_dir)
