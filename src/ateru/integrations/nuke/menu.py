import nuke
import importlib

if nuke.GUI:
    import ateru.ui.dcc.nuke_panel as nuke_panel_module
    from ateru.ui.windows.show_manager import main  # Manager sigue funcionando

    menu = nuke.menu("Nuke")
    ateru_menu = menu.addMenu("Ateru")

    ateru_menu.addCommand("Open Manager", "main()")  # Manager antiguo

    def open_pipeline_panel():
        importlib.reload(nuke_panel_module)  # recarga el módulo
        nuke_panel_module.load_nuke_panel()  # luego llama a la función para abrir el panel

    ateru_menu.addCommand("Open Pipeline Panel", open_pipeline_panel)
