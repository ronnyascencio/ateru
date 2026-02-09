from pathlib import Path
from ateru.core.config.model import Ateru, GlobalConfig, SoftwareConfig
from ateru.core.config.loader import ensure_config_exists
from ateru.core.project.model import Project
from ateru.core.shot.model import Shot
from ateru.core.asset.model import Asset
from ateru.core.project import load
import tomli_w
import tomli
from ateru.core.logging import events


CONFIG_FILE = Path.home() / "._ateru" / "ateru_config.toml"


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


def load_config() -> dict:
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("rb") as f:
            return tomli.load(f)
    else:
        # Crear archivo base vacío
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        base = {"title": {"name": "Ateru Global Configuration"}}
        with CONFIG_FILE.open("wb") as f:
            tomli_w.dump(base, f)
        return base


def write_config(data: dict):
    """secure write data."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open("wb") as f:
        tomli_w.dump(data, f)
    events.success(f"Config File updated {CONFIG_FILE}")


def write_global_config_root(Ateru: GlobalConfig):
    """update root section TOML without delete apps."""
    config = ensure_config_exists()
    config["root"] = Ateru.model_dump(mode="json")
    with CONFIG_FILE.open("wb") as f:
        tomli_w.dump(config, f)


def write_global_config_software(apps: SoftwareConfig):
    """update apps section TOML without delete root."""
    config = ensure_config_exists()
    config["apps"] = apps.model_dump(mode="json")
    with CONFIG_FILE.open("wb") as f:
        tomli_w.dump(config, f)
