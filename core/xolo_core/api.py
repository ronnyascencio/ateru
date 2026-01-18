from core.xolo_core.project.model import Project, Xolo
from core.xolo_core.shot.model import Shot
from core.xolo_core.asset.model import Asset
from core.xolo_core.project.create import create_project_structure
from core.xolo_core.shot.create import create_shot_structure
from core.xolo_core.asset.create import create_asset_structure
from core.xolo_core.project.scan import list_projects
from core.xolo_core.shot.scan import list_shots
from core.xolo_core.asset.scan import list_assets
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
    shot_path = root.root / "shots" / shot_name

    shot = Shot(
        root=shot_path,
        shot_name=shot_name,
        start=start,
        end=end,
        fps=fps,
    )

    create_shot_structure(project_name=project_name, shot_name=shot_name)
    create.write_shot_config(project_name=project_name, shot=shot)


def scan_shots(project_name: str):
    projects_root = loader.read_xolo_config()
    shots_path = projects_root / project_name / "shots"
    shots = list_shots(shots_path)
    events.info(f" shots in {project_name} directory: {shots}")
    return shots


def create_asset(
    project_name: str,
    asset_name: str,
    type: str,
):
    root = read_project_config(project_name)
    root_assets = root.root / asset_name
    assets_path = root.root / "assets" / asset_name

    asset = Asset(asset_name=asset_name, asset_type=type, root=assets_path)
    create_asset_structure(project_name=project_name, asset_name=asset_name)
    create.write_asset_config(asset=asset, project_name=project_name)


def scan_assets(project_name: str):
    projects_root = loader.read_xolo_config()
    assets_path = projects_root / project_name / "assets"
    assets = list_assets(assets_path)
    events.info(f" assets in {project_name} directory: {assets}")
    return assets


def set_globalconfig(root: Path):
    xolo = model.Xolo(projects_root=root)
    create.write_global_config(xolo)


