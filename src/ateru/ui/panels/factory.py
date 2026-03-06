
from ateru.ui.panels.gaffer.gaffer_tools import GafferTools
from ateru.ui.panels.blender.blender_tools import BlenderTools
from ateru.ui.panels.nuke.nuke_tools import NukeTools

def get_tools_widget(dcc_name: str):
    dcc_name = dcc_name.lower()
    if dcc_name == "gaffer":
        return GafferTools()
    elif dcc_name == "blender":
        return BlenderTools()
    elif dcc_name == "nuke":
        return NukeTools()
    else:
        raise ValueError(f"DCC unknow: {dcc_name}")
