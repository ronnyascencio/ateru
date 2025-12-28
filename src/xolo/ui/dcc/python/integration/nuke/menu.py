import os
import sys
from pathlib import Path

import nuke


PIPELINE_ROOT = os.environ.get("PROJECT_ROOT") or os.environ.get("PIPELINE_ROOT")
if not PIPELINE_ROOT:
    raise RuntimeError("PROJECT_ROOT / PIPELINE_ROOT is not defined")

PIPELINE_ROOT = Path(PIPELINE_ROOT)

# Agregar pipeline y venv a sys.path para PySide6, rich, etc.
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

VENV_SITE = PIPELINE_ROOT / ".venv" / "lib" / "python3.11" / "site-packages"
if VENV_SITE.exists() and str(VENV_SITE) not in sys.path:
    sys.path.insert(0, str(VENV_SITE))


try:
    from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
    from core.xolo_core.ui.xolo_window import XoloMainWindow
    UI_AVAILABLE = True
except Exception as e:
    print(f"[XOLO MENU] UI not available: {e}")
    UI_AVAILABLE = False


_XOLO_WINDOW = None

def launch_xolo_ui():
    global _XOLO_WINDOW
    if not UI_AVAILABLE:
        print("[XOLO MENU] UI not available")
        return

    try:
        if _XOLO_WINDOW is None:
            _XOLO_WINDOW = XoloMainWindow(dcc="nuke")
            _XOLO_WINDOW.setWindowTitle("Xolo Pipeline")
            _XOLO_WINDOW.show()
        else:
            _XOLO_WINDOW.raise_()
            _XOLO_WINDOW.activateWindow()
        print("[XOLO MENU] Xolo UI shown")
    except Exception as e:
        print(f"[XOLO MENU] ERROR opening UI: {e}")


def create_xolo_menu():
    try:
        # Crear menú principal "Xolo" en top bar
        xolo_menu = nuke.menu("Nuke").addMenu("Xolo", icon=None)

        # Submenu "Saver" que abre la UI
        xolo_menu.addCommand("Saver", launch_xolo_ui, icon=None)

        print("[XOLO MENU] Menu created successfully")
    except Exception as e:
        print(f"[XOLO MENU] ERROR creating menu: {e}")


create_xolo_menu()
