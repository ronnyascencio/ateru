import os
from pathlib import Path

import bpy

from core.xolo_core.generators.version_generator import VersionManager


def get_project_root():
    """Reads PROJECT_ROOT env var set by xolo launch."""
    return os.environ.get("PROJECT_ROOT", "")


def get_available_shots():
    project = get_project_root()
    if not project:
        return []

    return VersionManager.get_shots(project)


def get_versions_for_shot(shot):
    """
    The VersionManager expects the FULL shot path.
    Example: /projects/projectname/shots/sh010
    """
    project_root = get_project_root()
    if not project_root:
        return []

    shot_path = str(Path(project_root) / "shots" / shot)

    versions = VersionManager.get_version(shot_path, "blender")
    if isinstance(versions, str):
        return []  # no versions found or unsupported

    return versions


# ---------------------------------------------------------
#  Operators
# ---------------------------------------------------------


class XOLO_OT_SetShot(bpy.types.Operator):
    bl_idname = "xolo.set_shot"
    bl_label = "Set Shot"

    shot: bpy.props.StringProperty()

    def execute(self, context):
        context.scene.xolo_current_shot = self.shot

        versions = get_versions_for_shot(self.shot)
        context.scene.xolo_current_version = versions[0] if versions else ""
        return {"FINISHED"}


class XOLO_OT_SetVersion(bpy.types.Operator):
    bl_idname = "xolo.set_version"
    bl_label = "Set Version"

    version: bpy.props.StringProperty()

    def execute(self, context):
        context.scene.xolo_current_version = self.version
        return {"FINISHED"}


# ---------------------------------------------------------
#  Register
# ---------------------------------------------------------

classes = (
    XOLO_OT_SetShot,
    XOLO_OT_SetVersion,
)


def register():
    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except:
            pass

        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except:
            pass

        bpy.utils.register_class(cls)
