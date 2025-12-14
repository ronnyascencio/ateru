import functools
import os
import subprocess
import sys
from pathlib import Path

import Gaffer
import GafferUI

PIPELINE_ROOT = os.environ.get("PIPELINE_ROOT")
venv_path = Path(str(PIPELINE_ROOT)) / ".venv" / "lib" / "python3.11" / "site-packages"
venv_site_packages = os.path.expanduser(venv_path)

if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)


from rich.console import Console

console = Console()


# -----------------------------
# Function menu command
# -----------------------------
def launchTextureGenerator(menu):
    PIPELINE_ROOT = os.environ.get("PIPELINE_ROOT")
    XOLO_GENERATOR_PATH = os.path.join(
        PIPELINE_ROOT, "core", "xolo_core", "generators", "texture_generator.py"
    )

    if not os.path.exists(XOLO_GENERATOR_PATH):
        print(
            "[XOLO MENU] ERROR: texture_generator not found:",
            XOLO_GENERATOR_PATH,
        )
        return

    subprocess.Popen([sys.executable, XOLO_GENERATOR_PATH])
    print("[XOLO MENU] texture_generator launched.")


# -----------------------------
# menu inyection
# -----------------------------
try:
    # ❗ passing application instance is required in Gaffer 1.0+
    GafferUI.ScriptWindow.menuDefinition(application).append(
        "/Xolo/Make TEX...",
        {
            "command": functools.partial(launchTextureGenerator),
            "label": "Make TEX...",
            "shortCut": "",
        },
    )
    console.print("[XOLO MENU]  menu loaded", style="green")


except Exception as e:
    console.print(f"[XOLO MENU] ERROR menu not loaded : {e}", style="red")
