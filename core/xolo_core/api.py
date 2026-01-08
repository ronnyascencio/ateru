from core.xolo_core.project.model import Project
from core.xolo_core.project.create import create_project_structure, write_project_config
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
    root: Path,
    fps: int,
    width: str,
    height: str,
):
    rand_id: int = uuid.uuid4().int
    root_project = root / project_name
    project = Project(
        id=rand_id,
        name=project_name,
        root=root_project,
        fps=fps,
        resolution=(width, height),
    )
    create_project_structure(root, project.name)
    write_project_config(project=project)
