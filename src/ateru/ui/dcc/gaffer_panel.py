from GafferUI import Window, Widget
from ateru.ui.panels.base_panel import BasePanel
from ateru.ui.panels.shered.context_section import ContextSection
from ateru.ui.panels.shered.publish_section import PublishSection
from ateru.ui.panels.gaffer.gaffer_tools import GafferTools
from ateru.ui.panels.factory import get_tools_widget


_gaffer_panel_window = None


def load_gaffer_panel():
    global _gaffer_panel_window

    # Crear widgets internos
    context_widget = ContextSection()
    publish_widget = PublishSection()
    tools_widget = get_tools_widget("gaffer")

    # Crear panel base (QWidget)
    base_panel = BasePanel(
        tools_widget=tools_widget,
        context_widget=context_widget,
        publish_widget=publish_widget,
    )

    # Envolver en GafferUI.Widget
    panel = Widget(base_panel)

    # Crear ventana Gaffer
    window = Window("Ateru Pipeline - Gaffer")
    window.setChild(panel)
    window.setVisible(True)

    # Guardar la referencia global para que no sea recolectada
    _gaffer_panel_window = window
