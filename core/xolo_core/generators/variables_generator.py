import os
from pathlib import Path

from rich.console import Console

console = Console()


def project_root_variable(project_root: str):
    root_project_folder = project_root
    project_root_env = Path(root_project_folder).resolve()
    assets_root_env = Path(root_project_folder, "assets").resolve()
    os.environ["PROJECT_ROOT"] = str(project_root_env)
    os.environ["ASSETS_ROOT"] = str(assets_root_env)
    console.print(
        f"DEBUG: Set PROJECT_ROOT to {os.environ['PROJECT_ROOT']}", style="green"
    )
    console.print(
        f"DEBUG: Set ASSETS_ROOT to {os.environ['ASSETS_ROOT']}", style="green"
    )

    return os.environ.get("PROJECT_ROOT"), os.environ.get("ASSETS_ROOT")


def ocio_variable(dcc: str):
    if dcc == "Blender":
        ocio_path = (
            Path(__file__).resolve().parent.parent.parent
            / "ocio"
            / "studio-config-all-views-v3.0.0_aces-v2.0_ocio-v2.4.ocio"
        )
    else:
        ocio_path = (
            Path(__file__).resolve().parent.parent.parent
            / "ocio"
            / "studio-config-v2.2.0_aces-v1.3_ocio-v2.3.ocio"
        )

    os.environ["OCIO"] = str(ocio_path)
    console.print(f"DEBUG: Set OCO to {os.environ['OCIO']}", style="green")
    return os.environ.get("OCIO")


def prman_variable():
    opt_path = "/opt/pixar/RenderManProServer-27.0"
    prman_path = Path(opt_path).resolve()
    return str(prman_path)
