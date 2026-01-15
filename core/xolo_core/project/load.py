try:
    import tomllib
except ImportError:
    import tomli as tomllib
from pathlib import Path
from core.xolo_core.project.paths import resolve_xolo_path
from core.xolo_core.config.model import ProjectConfig, ShotConfig


def read_xolo_config():
    config_file = resolve_xolo_path() / ".xolo" / "xolo_config.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)
    projects_root: str = data["Paths"]["projects_root"]

    return Path(projects_root)


def read_project_config(project_name: str) -> ProjectConfig:
    config_file = read_xolo_config() / project_name / "config" / "pconfig.toml"

    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    return ProjectConfig(**data["project"])


def read_shot_config(project_name: str, shot_name: str) -> ShotConfig:
    config_file = read_xolo_config() / project_name / "config" / "pconfig.toml"

    with open(config_file, "rb") as f:
        project_data = tomllib.load(f)
    config_file = project_data["project"]["shots"] / shot_name / "sconfig.toml"

    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    return ShotConfig(**data["shot"])
