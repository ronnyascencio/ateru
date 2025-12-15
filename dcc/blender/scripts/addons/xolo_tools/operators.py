import bpy
from .launch_ui import launch_window

class XOLO_OT_OpenUI(bpy.types.Operator):
    bl_idname = "xolo.open_ui"
    bl_label = "Open Xolo UI"

    def execute(self, context):
        launch_window()
        print("UI abierta ✅")
        return {'FINISHED'}
