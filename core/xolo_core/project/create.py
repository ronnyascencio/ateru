from typing import Tuple
from pydantic import BaseModel
from pathlib import Path
from core.xolo_core.project.model import Project
from core.xolo_core.project.paths import resolve_project_paths
from core.xolo_core.config.model import ProjectConfig
from core.xolo_core.logging import events
import uuid
import tomli_w


"""
core creation for projects, shots, assets


"""


def create_project_structure(root: Path, project_name: str):
    project_root = root / project_name
    events.success(f"Project Path:  {project_root}")
    model = ProjectConfig(root=project_root)
    directories = resolve_project_paths(model)
    for folder in directories.values():
        path = folder
        path.mkdir(exist_ok=True)
        events.info(f"Created directory: {str(path)}")


def write_project_config(project: Project):
    config_file = project.root / "config" / "project.toml"

    data: dict = {
        "project": project.model_dump(mode="json"),
    }
    config_file.parent.mkdir(parents=True, exist_ok=True)

    with config_file.open("wb") as f:
        tomli_w.dump(data, f)
    events.success(f"Config File created {config_file}")
