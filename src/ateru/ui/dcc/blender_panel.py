import bpy
from PySide6.QtWidgets import QApplication
from ateru.ui.panels.base_panel import BasePanel
from ateru.ui.panels.shered.context_section import ContextSection
from ateru.ui.panels.shered.publish_section import PublishSection
from ateru.ui.panels.blender.blender_tools import BlenderTools
import sys

def load_blender_panel():
    parent = bpy.context.window_manager.windows[0]  # Para ejemplo, usar primer window
    context_widget = ContextSection()
    tools_widget = BlenderTools()
    publish_widget = PublishSection()

    panel = BasePanel(context_widget, tools_widget, publish_widget, parent=parent)
    panel.show()
    return panel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_blender_panel()
    sys.exit(app.exec())
