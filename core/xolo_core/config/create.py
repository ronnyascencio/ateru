from pathlib import Path
from core.xolo_core.config.model import Xolo, GlobalConfig, SoftwareConfig
from core.xolo_core.project.model import Project
from core.xolo_core.shot.model import Shot
from core.xolo_core.asset.model import Asset
from core.xolo_core.project import load
import tomli_w
from core.xolo_core.logging import events


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
    project = load.read_project_config(project_name)
    shot_name = shot.shot_name
    config_file = project.root / "shots" / shot_name / "sconfig.toml"

    data: dict = {
        "Shot": shot.model_dump(mode="json"),
    }

    config_file.parent.mkdir(parents=True, exist_ok=True)

    with config_file.open("wb") as f:
        tomli_w.dump(data, f)
    events.success(f"Config File created {config_file}")


def write_asset_config(asset: Asset, project_name: str):
    project = load.read_project_config(project_name)
    asset_name = asset.asset_name
    config_file = project.root / "assets" / asset_name / "aconfig.toml"

    data: dict = {
        "Asset": asset.model_dump(mode="json"),
    }

    config_file.parent.mkdir(parents=True, exist_ok=True)

    with config_file.open("wb") as f:
        tomli_w.dump(data, f)
    events.success(f"Config File created {config_file}")


"""

    Gobal configuration

"""


def write_global_config(xolo: GlobalConfig, apps: SoftwareConfig):
    config_file: Path = Path.home() / ".xolo" / "xolo_config.toml"
    title: dict = {"name": "Xolo Global Configuration"}

    data: dict = {
        "title": title,
        "root": xolo.model_dump(mode="json"),
        "apps": apps.model_dump(mode="json")
    }

    config_file.parent.mkdir(parents=True, exist_ok=True)

    with config_file.open("wb") as f:
        tomli_w.dump(data, f)
    events.success(f"Config File created {config_file}")
