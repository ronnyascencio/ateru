import os
from pathlib import Path
from core.xolo_core.config.model import ProjectConfig, ShotConfig


def resolve_project_paths(config: ProjectConfig) -> dict[str, Path]:
    return {
        "root": config.root,
        "assets": config.root / config.assets_dir,
        "shots": config.root / config.shots_dir,
        "renders": config.root / config.renders_dir,
        "editorial": config.root / config.editorial_dir,
        "plates": config.root / config.plates_dir,
        "config": config.root / config.config_dir,
    }


def resolve_global_config_path():
    xolo_dir: Path = Path()
    return xolo_dir


def resolve_xolo_path():
    home_dir = os.getenv("HOME")

    xolo_dir: Path = Path(str(home_dir))

    return xolo_dir


def resolve_shot_path(config: ShotConfig) -> dict[str, Path]:
    return {
        "root": config.root,
        "work": config.root / config.work_dir,
        "publish": config.root / config.publish_dir,
    }


def resolve_publish_path(config: ShotConfig) -> dict[str, Path]:
    return {
        "publish": config.root / config.publish_dir,
    }
