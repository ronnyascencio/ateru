import functools
import os
import sys
from pathlib import Path

import GafferUI


# PIPELINE ROOT environment variable

PIPELINE_ROOT = os.environ.get("PIPELINE_ROOT")

if not PIPELINE_ROOT:
    raise RuntimeError("PIPELINE_ROOT is not defined")

PIPELINE_ROOT = Path(PIPELINE_ROOT)

# pipeline root to sys path for gaffer
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

# venv site-packages
venv_site = PIPELINE_ROOT / ".venv" / "lib" / "python3.11" / "site-packages"
if venv_site.exists() and str(venv_site) not in sys.path:
    sys.path.insert(0, str(venv_site))


# Logging

try:
    from rich.console import Console
    console = Console()
except Exception:
    console = None

def log(msg, style="green"):
    if console:
        console.print(msg, style=style)
    else:
        print(msg)


# UI IMPORT

try:
    from core.xolo_core.ui.xolo_window import XoloMainWindow
    UI_AVAILABLE = True
    log("[XOLO MENU] UI imported successfully", "green")
except Exception as e:
    UI_AVAILABLE = False
    log(f"[XOLO MENU] ERROR importing UI: {e}", "red")


# SINGLETON de ventana (EVITA FREEZE)

_XOLO_WINDOW = None

def openXoloUI(menu=None):
    global _XOLO_WINDOW

    log("[XOLO MENU] openXoloUI called", "blue")

    if not UI_AVAILABLE:
        log("[XOLO MENU] UI not available", "red")
        return

    try:
        if _XOLO_WINDOW is None:
            _XOLO_WINDOW = XoloMainWindow()
            _XOLO_WINDOW.setWindowTitle("Xolo Pipeline")
            _XOLO_WINDOW.show()
        else:
            _XOLO_WINDOW.raise_()
            _XOLO_WINDOW.activateWindow()

        log("[XOLO MENU] Xolo UI shown", "green")

    except Exception as e:
        log(f"[XOLO MENU] ERROR opening UI: {e}", "red")


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
        log(f"[XOLO MENU] texture_generator not found: {generator}", "red")
        return

    os.system(f'"{sys.executable}" "{generator}"')
    log("[XOLO MENU] Texture generator launched")


# Menu Injection

try:
    menu_def = GafferUI.ScriptWindow.menuDefinition(application)

    menu_def.append(
        "/Xolo/Open UI",
        {"command": openXoloUI}
    )

    menu_def.append(
        "/Xolo/Make Texture",
        {"command": launchTextureGenerator}
    )

    log("[XOLO MENU] Menu loaded", "green")

except Exception as e:
    log(f"[XOLO MENU] ERROR loading menu: {e}", "red")
