from pathlib import Path
from core.xolo_core.config.model import ProjectConfig


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
