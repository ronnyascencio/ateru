import functools
import os
import sys
from pathlib import Path
from core.xolo_core.utils.logging import log_core, log_ui, log_error
import GafferUI

PIPELINE_ROOT = Path(os.environ["PIPELINE_ROOT"])
VENV_SITE = PIPELINE_ROOT / ".venv" / "lib/python3.11/site-packages"


if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

if VENV_SITE.exists() and str(VENV_SITE) not in sys.path:
    sys.path.insert(0, str(VENV_SITE))


from core.xolo_core.extractors.dcc import detect_dcc

# UI IMPORT

try:
    from core.xolo_core.ui.xolo_window import XoloMainWindow
    UI_AVAILABLE = True
    log_ui("[XOLO MENU] UI imported successfully")
except Exception as e:
    UI_AVAILABLE = False
    log_error(f"[XOLO MENU] ERROR importing UI: {e}")


# SINGLETON de ventana (EVITA FREEZE)

_XOLO_WINDOW = None

def saverXoloUI(menu=None):
    global _XOLO_WINDOW

    log_ui("[XOLO MENU] Xolo Server called")

    if not UI_AVAILABLE:
        log_error("[XOLO MENU] UI not available")
        return

    try:
        if _XOLO_WINDOW is None:
            current_dcc = detect_dcc()
            _XOLO_WINDOW = XoloMainWindow(dcc=current_dcc)
            _XOLO_WINDOW.setWindowTitle("Xolo Pipeline")
            _XOLO_WINDOW.show()
        else:
            _XOLO_WINDOW.raise_()
            _XOLO_WINDOW.activateWindow()

        log_ui("[XOLO MENU] Xolo UI shown")

    except Exception as e:
        log_error(f"[XOLO MENU] ERROR opening UI: {e}")


# Texture Generator (igual que antes)

def launchTextureGenerator(menu=None):
    generator = (
        PIPELINE_ROOT
        / "core"
        / "xolo_core"
        / "generators"
        / "texture_generator.py"
    )

    if not generator.exists():
        log_error(f"[XOLO MENU] texture_generator not found: {generator}")
        return

    os.system(f'"{sys.executable}" "{generator}"')
    log_ui("[XOLO MENU] Texture generator launched")


# Menu Injection

try:
    menu_def = GafferUI.ScriptWindow.menuDefinition(application)

    menu_def.append(
        "/Xolo/Saver",
        {"command": saverXoloUI}
    )

    menu_def.append(
        "/Xolo/Make Texture",
        {"command": launchTextureGenerator}
    )

    log_core("[XOLO MENU] Menu loaded")

except Exception as e:
    log_error(f"[XOLO MENU] ERROR loading menu: {e}")
