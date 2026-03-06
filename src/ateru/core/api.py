from ateru.core.project.model import Project
from ateru.core.shot.model import Shot
from ateru.core.asset.model import Asset
from ateru.core.config.model import GlobalConfig, SoftwareConfig
from ateru.core.project.create import create_project_structure
from ateru.core.project.delete import project_delete
from ateru.core.shot.create import create_shot_structure
from ateru.core.shot.delete import shot_delete
from ateru.core.asset.create import create_asset_structure
from ateru.core.project.scan import list_projects
from ateru.core.shot.scan import list_shots
from ateru.core.asset.scan import list_assets
from ateru.core.config import loader, create, model
from ateru.core.project.load import read_project_config, update_status
import os
from ateru.core.logging import events
from pathlib import Path
import uuid


"""

    Project API:
        create project
        delete project
        scan project
        create shot
        delete shot
        scan shot
        create asset
        delete asset
        scan asset

        show project info
        show shot info
        show pipeline info

    Validation API:
        scane name validation

"""


""" Project """


def create_project(project_name: str, fps: int, width: str, height: str, type: str):
    rand_id: int = uuid.uuid4().int

    root_project = Path(loader.read_ateru_config()) / project_name
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
        type=type,
        status="active",
    )
    create_project_structure(project.name)
    create.write_project_config(project=project)


def delete_project(project_name: str):
    project_delete(project_name)


def scan_projects():
    projects_root = loader.read_ateru_config()
    projects = list_projects(projects_root)

    return projects


""" Shot """


def create_shot(
    project_name: str,
    shot_name: str,
    start: int,
    end: int,
    fps: int,
    priority: str,
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
        priority=priority,
    )

    create_shot_structure(project_name=project_name, shot_name=shot_name)
    create.write_shot_config(project_name=project_name, shot=shot)


def scan_shots(project_name: str):
    projects_root = loader.read_ateru_config()
    shots_path = projects_root / project_name / "shots"
    shots = list_shots(shots_path)
    events.info(f" shots in {project_name} directory: {shots}")
    return shots


def delete_shot(project_name: str, shot_name: str):
    shot_delete(project_name=project_name, shot_name=shot_name)


def count_shots(project_name: str):
    projects_root = loader.read_ateru_config()
    shots_path = projects_root / project_name / "shots"
    shots = list_shots(shots_path)
    path = Path(shots_path)
    count = sum(1 for entry in path.iterdir() if entry.is_dir())
    return count


""" Asset """


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
    projects_root = loader.read_ateru_config()
    assets_path = projects_root / project_name / "assets"
    assets = list_assets(assets_path)
    events.info(f" assets in {project_name} directory: {assets}")
    return assets



""" env """


def merge_pythonpath(env, new_path):
    existing = env.get("PYTHONPATH", "")
    if existing:
        env["PYTHONPATH"] = new_path + os.pathsep + existing
    else:
        env["PYTHONPATH"] = new_path

""" Global """


def set_software_paths(nuke: Path, blender: Path, gaffer: Path):
    apps = model.SoftwareConfig(
        nuke=nuke, blender=blender, gaffer=gaffer
    )
    create.write_global_config_software(apps)


def set_projects_root(root: Path, ocio: Path):
    ateru = model.GlobalConfig(projects_root=root, ocio_config=ocio)

    create.write_global_config_root(ateru)


def project_data(project_name: str):
    return read_project_config(project_name)


def update_project_status(project_name: str, new_status: str):
    return update_status(project_name, new_status)
