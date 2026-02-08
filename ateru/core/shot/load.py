from ateru.core.config.loader import read_xolo_config
import tomllib
from ateru.core.config.model import ShotConfig


def read_shot_config(project_name: str, shot_name: str) -> ShotConfig:
    config_file = read_xolo_config() / project_name / "config" / "pconfig.toml"

    with open(config_file, "rb") as f:
        project_data = tomllib.load(f)
    config_file = project_data["project"]["shots"] / shot_name / "sconfig.toml"

    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    return ShotConfig(**data["shot"])
