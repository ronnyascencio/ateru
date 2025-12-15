import bpy

class XOLO_MT_Menu(bpy.types.Menu):
    bl_label = "Xolo Tools"
    bl_idname = "XOLO_MT_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("xolo.open_ui", text="Open Xolo UI")
