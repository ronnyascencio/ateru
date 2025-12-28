import bpy
from .launch_ui import launch_window
from core.xolo_core.utils.logging import log_core
class XOLO_OT_OpenUI(bpy.types.Operator):
    bl_idname = "xolo.open_ui"
    bl_label = "Open Xolo UI"

    def execute(self, context):
        launch_window()
        log_core("UI Opened")
        return {'FINISHED'}
