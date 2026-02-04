from typing import Tuple
from pydantic import BaseModel
from pathlib import Path
from xolo.core.config.model import Xolo
from xolo.core.project.model import Project
from xolo.core.config.paths import (
    resolve_project_paths,
    resolve_xolo_path,
    resolve_shot_path,
)
from xolo.core.config.model import ProjectConfig, ShotConfig
from xolo.core.logging import events
from xolo.core.config.loader import read_xolo_config
from xolo.core.project.load import read_project_config
import uuid
import tomli_w


"""
core creation for shots


"""


def create_shot_structure(project_name: str, shot_name: str):
    project_config = read_project_config(project_name)
    root_shot = project_config.root / project_config.shots / shot_name

    model = ShotConfig(root=root_shot)

    directories = resolve_shot_path(model)

    for path in directories.values():
        path.mkdir(parents=True, exist_ok=True)
        events.info(f"Created directory: {path}")
