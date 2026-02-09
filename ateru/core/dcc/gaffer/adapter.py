# _ateru/core/dcc/gaffer/adapter.py
import Gaffer
from pathlib import Path
from ateru.core.dcc.base import DCCAdapterBase


class GafferAdapter(DCCAdapterBase):
    name = "gaffer"

    def open_scene(self, path: Path):
        script = Gaffer.ScriptNode()
        script["fileName"].setValue(str(path))
        script.load()

    def save_scene(self, path: Path):
        script = Gaffer.ScriptNode()
        script["fileName"].setValue(str(path))
        script.save()
