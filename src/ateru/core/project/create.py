from typing import Tuple
from pydantic import BaseModel
from pathlib import Path
from ateru.core.config.model import Ateru
from ateru.core.project.model import Project
from ateru.core.config.paths import (
    resolve_project_paths,
    resolve_ateru_path,
    resolve_shot_path,
)
from ateru.core.config.model import ProjectConfig, ShotConfig
from ateru.core.logging import events
from ateru.core.config.loader import read_ateru_config
from ateru.core.project.load import read_project_config
import uuid
import tomli_w


"""
core creation for projects, shots, assets


"""


def create_project_structure(project_name: str):
    project_root = Path(read_ateru_config()) / project_name
    events.success(f"Project Path:  {project_root}")
    model = ProjectConfig(root=project_root)
    directories = resolve_project_paths(model)
    for path in directories.values():
        path.mkdir(exist_ok=True)
        events.info(f"Created directory: {str(path)}")


