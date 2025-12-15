import os
import re
from pathlib import Path
from core.xolo_core.extractors.dcc import load_map

"""Global Variables"""

ASSETS_DIR = os.environ.get("ASSETS_ROOT")

class VersionManager:
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
    def get_version(shot: str, dcc: str):
        """returns list of versions available for a given shot"""

        dcc_map = load_map(dcc)
        if dcc not in dcc_map:
            return "DCC not supported"

        extension = dcc_map
        versions = []

        versions = []
        versions_dir = Path(shot) / "work" / dcc
        print(f"Version pulled from: {versions_dir}")
        if not versions_dir.exists() or not versions_dir.is_dir():
            return "no versions found"

        pattern = r"_v(\d{3})$"

        for file_path in versions_dir.iterdir():
            if file_path.is_file() and file_path.suffix == extension:
                # file_path.stem nos da el nombre sin extensión (ej: shot_name_v001)
                match = re.search(pattern, file_path.stem)

                if match:
                    versions.append(file_path.name)

        return sorted(versions)
    @staticmethod
    def get_work_asset(department: str, asset_name: str):
        """returns list of assets available in the assets directory"""

        asset_work_dir = Path(str(ASSETS_DIR)) / "work"
        assets = []
        return print(asset_work_dir)
