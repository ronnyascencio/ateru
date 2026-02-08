try:
    import tomllib
    import tomli_w
except ImportError:
    import tomli as tomllib
from pathlib import Path
from ateru.core.config.paths import resolve_xolo_path
from ateru.core.config.model import ProjectConfig, ShotConfig
from ateru.core.config import loader
from ateru.core.project.model import Project


def read_project_config(project_name: str) -> Project:
    config_file = loader.read_xolo_config() / project_name / "config" / "pconfig.toml"

    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    return Project(**data["project"])


def update_status(project_name: str, new_status: str):
    config_file = loader.read_xolo_config() / project_name / "config" / "pconfig.toml"

    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    data["project"]["status"] = new_status

    with open(config_file, "wb") as f:
        tomli_w.dump(data, f)
