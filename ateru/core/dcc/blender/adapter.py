# ateru/core/dcc/blender/adapter.py
import bpy
from pathlib import Path
from ateru.core.dcc.base import DCCAdapterBase


class BlenderAdapter(DCCAdapterBase):
    name = "blender"

    def open_scene(self, path: Path):
        bpy.ops.wm.open_mainfile(filepath=str(path))

    def save_scene(self, path: Path):
        bpy.ops.wm.save_as_mainfile(filepath=str(path))
