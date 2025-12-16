import bpy
from xolo_core.ui.xolo_window import XoloMainWindow
from xolo_core.utils.logging import log_core, log_ui, log_error

from .operators import XOLO_OT_OpenUI
from .menu import XOLO_MT_Menu


# ------------------------------
# Ahora sí podemos importar módulos
# ------------------------------
# Prueba PySide6
try:
    from PySide6 import QtWidgets
    log_core("PySide6 found")
except ModuleNotFoundError:
    log_error("PySide6 NO found")




""" Classes register"""
classes = [XOLO_OT_OpenUI, XOLO_MT_Menu]

def draw_menu(self, context):
    self.layout.menu("XOLO_MT_menu")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_menu)
    log_core("Xolo Tools registered")

def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    log_core("Xolo Tools registered")
