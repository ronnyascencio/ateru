# _ateru/core/dcc/factory.py
from ateru.core.dcc.nuke.adapter import NukeAdapter
from ateru.core.dcc.blender.adapter import BlenderAdapter
from ateru.core.dcc.gaffer.adapter import GafferAdapter


def detect_dcc():
    try:
        import nuke
        return NukeAdapter()
    except ImportError:
        pass

    try:
        import bpy
        return BlenderAdapter()
    except ImportError:
        pass

    try:
        import Gaffer
        return GafferAdapter()
    except ImportError:
        pass

    raise RuntimeError("No supported DCC detected")
