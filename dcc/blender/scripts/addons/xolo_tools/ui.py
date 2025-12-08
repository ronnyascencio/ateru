import os

import bpy
from bpy.types import Menu, Panel

from core.xolo_core.generators.version_generator import VersionManager


# -------------------------------------------------------
# UTILS: get  PROJECT_ROOT
# -------------------------------------------------------
def get_project_root():
    return os.environ.get("PROJECT_ROOT", "")


# -------------------------------------------------------
# TOPBAR MENU > XOLO > SHOTS
# -------------------------------------------------------
class XOLO_MT_Shots(Menu):
    bl_label = "Shots"
    bl_idname = "XOLO_MT_shots"

    def draw(self, context):
        layout = self.layout
        project_root = get_project_root()

        shots = VersionManager.get_shots(project_root)

        if not shots:
            layout.label(text="No shots found", icon="ERROR")
            return

        for shot in shots:
            op = layout.operator("xolo.select_shot", text=shot)
            op.shot = shot


# -------------------------------------------------------
# TOPBAR MENU PRINCIPAL
# -------------------------------------------------------
class XOLO_MT_MainMenu(Menu):
    bl_label = "Xolo Pipeline"

    def draw(self, context):
        layout = self.layout
        layout.menu("XOLO_MT_shots", icon="FILE_FOLDER")


# -------------------------------------------------------
# N-PANEL
# -------------------------------------------------------
class XOLO_PT_Panel(Panel):
    bl_label = "Xolo Pipeline"
    bl_idname = "XOLO_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Xolo"

    def draw(self, context):
        layout = self.layout
        project_root = get_project_root()

        # Shots
        shots = VersionManager.get_shots(project_root)
        layout.prop(context.scene, "xolo_shot", text="Shot")

        # Versions (shot context)
        shot = context.scene.xolo_shot
        if shot:
            versions = VersionManager.get_version(
                os.path.join(project_root, "shots", shot), "blender"
            )
            layout.prop(context.scene, "xolo_version", text="Version")


# -------------------------------------------------------
# DYNAMIC PROPERTIES
# -------------------------------------------------------
def update_shot(self, context):
    """Reset version when shot changes"""
    context.scene.xolo_version = ""


def get_shot_items(self, context):
    project_root = get_project_root()
    shots = VersionManager.get_shots(project_root)
    return [(s, s, "") for s in shots]


def get_version_items(self, context):
    project_root = get_project_root()
    shot = context.scene.xolo_shot

    if not shot:
        return []

    versions = VersionManager.get_version(
        os.path.join(project_root, "shots", shot), "blender"
    )

    if isinstance(versions, str):
        return []  # "no versions found"

    return [(v, v, "") for v in versions]


# properties register
def register_properties():
    bpy.types.Scene.xolo_shot = bpy.props.EnumProperty(
        name="Shot", items=get_shot_items, update=update_shot
    )

    bpy.types.Scene.xolo_version = bpy.props.EnumProperty(
        name="Version", items=get_version_items
    )


def unregister_properties():
    del bpy.types.Scene.xolo_shot
    del bpy.types.Scene.xolo_version


# -------------------------------------------------------
# REGISTER/UNREGISTER
# -------------------------------------------------------
classes = [
    XOLO_MT_MainMenu,
    XOLO_MT_Shots,
    XOLO_PT_Panel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    register_properties()

    # Blender 5.0 support
    bpy.types.TOPBAR_MT_editor_menus.append(draw_xolo_menu)


def unregister():
    # Blender 5.0 support
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_xolo_menu)

    unregister_properties()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


# Function for menu instertion
def draw_xolo_menu(self, context):
    layout = self.layout
    layout.menu("XOLO_MT_MainMenu")
