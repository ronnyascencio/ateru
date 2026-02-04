# core/xolo_core/dcc/nuke/adapter.py
from pathlib import Path
from xolo.core.dcc.base import DCCAdapterBase
import nuke

class NukeAdapter(DCCAdapterBase):
    def load_usd(self, path: Path):
        print(f"Cargando USD en Nuke: {path}")
        # nuke.nodePaste(path) o código real

    def save_usd(self, path: Path):
        print(f"Guardando USD en Nuke: {path}")

    def open_scene(self, path: Path):
        nuke.scriptOpen(str(path))

    def save_scene(self, path: Path):
        nuke.scriptSave(str(path))
