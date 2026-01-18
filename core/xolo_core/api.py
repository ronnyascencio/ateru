from core.xolo_core.project.model import Project, Xolo
from core.xolo_core.shot.model import Shot
from core.xolo_core.project.create import create_project_structure
from core.xolo_core.shot.create import create_shot_structure
from core.xolo_core.project.scan import list_projects
from core.xolo_core.config import loader, create, model
from core.xolo_core.project.load import read_project_config
from core.xolo_core.logging import events
from pathlib import Path
import uuid


"""

    Project API:
        create
        delete
        scan

"""


def create_project(
    project_name: str,
    fps: int,
    width: str,
    height: str,
):
    rand_id: int = uuid.uuid4().int

    root_project = Path(loader.read_xolo_config()) / project_name
    project = Project(
        id=rand_id,
        name=project_name,
        root=root_project,
        renders=root_project / "renders",
        assets=root_project / "assets",
        plates=root_project / "plates",
        shots=root_project / "shots",
        fps=fps,
        resolution=(width, height),
    )
    create_project_structure(project.name)
    create.write_project_config(project=project)


def scan_projects():
    projects_root = loader.read_xolo_config()
    projects = list_projects(projects_root)
    events.info(f" projects in projects directory: {projects}")
    return projects 


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
    create.write_shot_config(project_name=project_name, shot=shot)


def set_globalconfig(root: Path):
    xolo = model.Xolo(projects_root=root)
    create.write_global_config(xolo)


# create_project(project_name="test3", fps=24, width="1920", height="1080")
projects = scan_projects()
print(*projects, sep=" - ")
