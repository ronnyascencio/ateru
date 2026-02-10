def detect_dcc():
    try:
        import nuke
        from ateru.core.dcc.nuke.adapter import NukeAdapter
        return NukeAdapter()
    except ImportError:
        pass

    try:
        import bpy
        from ateru.core.dcc.blender.adapter import BlenderAdapter
        return BlenderAdapter()
    except ImportError:
        pass

    try:
        import Gaffer
        from ateru.core.dcc.gaffer.adapter import GafferAdapter
        return GafferAdapter()
    except ImportError:
        pass

    return None
