import Gaffer
import GafferUI
import functools
import importlib
from pathlib import Path

print("🔥 ATERU STARTUP LOADED")

# -----------------------------
# 1. Función para el menú
# -----------------------------
def versionUp(menu):
    print("Ateru Version Up clicked")

# -----------------------------
# 2. Función para abrir el panel
# -----------------------------
def open_pipeline_panel():
    # Importa el módulo del panel
    import ateru.ui.dcc.gaffer_panel as gaffer_panel_module

    # Recarga el módulo para reflejar cambios en desarrollo
    importlib.reload(gaffer_panel_module)

    # Llama a la función que abre el panel
    gaffer_panel_module.load_gaffer_panel()


# -----------------------------
# 3. Agregar entradas al menú
# -----------------------------
# 'application' ya está disponible en startup de Gaffer
menu_def = GafferUI.ScriptWindow.menuDefinition(application)

# Submenú Ateru
menu_def.append(
    "/Ateru/Version Up",
    {
        "command": versionUp,
        "label": "Version Up",
        "shortCut": "",
    },
)

menu_def.append(
    "/Ateru/Open Pipeline Panel",
    {
        "command": open_pipeline_panel,
        "label": "Open Pipeline Panel",
        "shortCut": "",
    },
)
