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
    project_root = project.root / project.name
    config_file = project_root / "config" / "project.toml"

    data: dict = {
        "project": project.model_dump(mode="json"),
    }
    config_file.parent.mkdir(parents=True, exist_ok=True)

    with config_file.open("wb") as f:
        tomli_w.dump(data, f)
    events.success(f"Config File created {config_file}")


def create_project(
    project_name: str,
    root: Path,
    fps: int,
    width: str,
    height: str,
):
    rand_id: int = uuid.uuid4().int
    project = Project(
        id=rand_id,
        name=project_name,
        root=root,
        fps=fps,
        resolution=(width, height),
    )
    create_project_structure(project.root, project.name)
    write_project_config(project=project)


project_creation = create_project(
    project_name="test",
    root=Path("/home/ronnyascencio/projects"),
    fps=24,
    width="1920",
    height="1080",
)
