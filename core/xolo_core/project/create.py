from typing import Tuple
from pydantic import BaseModel
from pathlib import Path
from core.xolo_core.project.model import Project, Xolo, Shot
from core.xolo_core.project.paths import (
    resolve_project_paths,
    resolve_xolo_path,
    resolve_shot_path,
)
from core.xolo_core.config.model import ProjectConfig, ShotConfig
from core.xolo_core.logging import events
from core.xolo_core.project.load import read_xolo_config, read_project_config
import uuid
import tomli_w


"""
core creation for projects, shots, assets


"""


def create_project_structure(project_name: str):
    project_root = Path(read_xolo_config()) / project_name
    events.success(f"Project Path:  {project_root}")
    model = ProjectConfig(root=project_root)
    directories = resolve_project_paths(model)
    for path in directories.values():
        path.mkdir(exist_ok=True)
        events.info(f"Created directory: {str(path)}")


def create_shot_structure(project_name: str, shot_name: str):
    project_config = read_project_config(project_name)
    root_shot = project_config.root / project_config.shots_dir / shot_name

    model = ShotConfig(root=root_shot)

    directories = resolve_shot_path(model)

    for path in directories.values():
        path.mkdir(parents=True, exist_ok=True)
        events.info(f"Created directory: {path}")


def write_project_config(project: Project):
    config_file = project.root / "config" / "pconfig.toml"

    data: dict = {
        "project": project.model_dump(mode="json"),
    }
    config_file.parent.mkdir(parents=True, exist_ok=True)

    with config_file.open("wb") as f:
        tomli_w.dump(data, f)
    events.success(f"Config File created {config_file}")


def write_shot_config(shot: Shot, project_name: str):
    project = read_project_config(project_name)
    shot_name = shot.shot_name
    config_file = project.root / "shots" / shot_name / "sconfig.toml"

    data: dict = {
        "Shot": shot.model_dump(mode="json"),
    }

    config_file.parent.mkdir(parents=True, exist_ok=True)

    with config_file.open("wb") as f:
        tomli_w.dump(data, f)
    events.success(f"Config File created {config_file}")


"""

    Gobal configuration

"""


def write_global_config(xolo: Xolo):
    config_file: Path = resolve_xolo_path() / ".xolo" / "xolo_config.toml"
    title: dict = {"name": "Xolo Global Configuration"}

    data: dict = {
        "title": title,
        "Paths": xolo.model_dump(mode="json"),
    }

    config_file.parent.mkdir(parents=True, exist_ok=True)

    with config_file.open("wb") as f:
        tomli_w.dump(data, f)
    events.success(f"Config File created {config_file}")
