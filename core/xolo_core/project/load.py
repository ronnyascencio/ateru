try:
    import tomllib
except ImportError:
    import tomli as tomllib
from pathlib import Path
from core.xolo_core.config.paths import resolve_xolo_path
from core.xolo_core.config.model import ProjectConfig, ShotConfig
from core.xolo_core.config import loader


def read_project_config(project_name: str) -> ProjectConfig:
    config_file = loader.read_xolo_config() / project_name / "config" / "pconfig.toml"

    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    return ProjectConfig(**data["project"])


