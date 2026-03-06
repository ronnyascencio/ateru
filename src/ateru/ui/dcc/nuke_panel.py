from ateru.ui.panels.base_panel import BasePanel
from ateru.ui.panels.shered.context_section import ContextSection
from ateru.ui.panels.shered.publish_section import PublishSection
from ateru.ui.panels.factory import get_tools_widget

import nuke
import shiboken6

_nuke_panel_instance = None


def load_nuke_panel():
    global _nuke_panel_instance


    if _nuke_panel_instance is not None:
        if shiboken6.isValid(_nuke_panel_instance):
            _nuke_panel_instance.show()
            _nuke_panel_instance.raise_()
            _nuke_panel_instance.activateWindow()
            return
        else:
            _nuke_panel_instance = None

 
    context_widget = ContextSection()
    publish_widget = PublishSection()
    tools_widget = get_tools_widget("nuke")

    panel = BasePanel(
        context_widget=context_widget,
        tools_widget=tools_widget,
        publish_widget=publish_widget,
    )

    panel.setWindowTitle("Ateru Pipeline - Nuke")

    _nuke_panel_instance = panel
    panel.show()
