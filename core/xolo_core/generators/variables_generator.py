from pathlib import Path
import os


def project_root_variable(project_root: str):
    root_project_folder = project_root
    project_root_env = Path(root_project_folder).resolve()
    assets_root_env = Path(root_project_folder, "assets").resolve()
    os.environ["PROJECT_ROOT"] = str(project_root_env)
    os.environ["ASSETS_ROOT"] = str(assets_root_env)
    print(f"DEBUG: Set PROJECT_ROOT to {os.environ['PROJECT_ROOT']}")
    print(f"DEBUG: Set ASSETS_ROOT to {os.environ['ASSETS_ROOT']}")

    return os.environ.get("PROJECT_ROOT"), os.environ.get("ASSETS_ROOT")
