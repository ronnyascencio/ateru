from core.xolo_core.project.model import Project, Xolo, Shot
from core.xolo_core.project.create import (
    create_project_structure,
    create_shot_structure,
    write_project_config,
    write_global_config,
    write_shot_config,
)
from core.xolo_core.project.load import read_xolo_config, read_project_config
from pathlib import Path
import uuid


"""

    Project API:
        create
        delete
        search

"""


def create_project(
    project_name: str,
    fps: int,
    width: str,
    height: str,
):
    rand_id: int = uuid.uuid4().int

    root_project = Path(read_xolo_config()) / project_name
    project = Project(
        id=rand_id,
        name=project_name,
        root=root_project,
        fps=fps,
        resolution=(width, height),
    )
    create_project_structure(project.name)
    write_project_config(project=project)


def create_shot(
    project_name: str,
    shot_name: str,
    start: int,
    end: int,
    fps: int,
):
    root = read_project_config(project_name)
    root_shot = root.root / shot_name

    shot = Shot(
        shot_name=shot_name,
        start=start,
        end=end,
        fps=fps,
    )

    create_shot_structure(project_name=project_name, shot_name=shot_name)
    write_shot_config(project_name=project_name, shot=shot)


def set_globalconfig(root: Path):
    xolo = Xolo(projects_root=root)
    write_global_config(xolo)



