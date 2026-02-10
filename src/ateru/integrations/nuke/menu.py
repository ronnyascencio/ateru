import nuke

if nuke.GUI:
    from ateru.ui.windows.show_manager import main
    from ateru.ui.windows.show_asset_manager import show

    menu = nuke.menu("Nuke")

    menu.addCommand("ateru/Open Manager", "main()")

    menu.addCommand("ateru/Pipeline", "show()")
