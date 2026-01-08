from pydantic import BaseModel
from pathlib import Path
from typing import Optional, Dict


class ProjectConfig(BaseModel):
    root: Path

    assets_dir: str = "assets"
    shots_dir: str = "shots"
    renders_dir: str = "renders"
    config_dir: str = "config"
    editorial_dir: str = "editorial"
    plates_dir: str = "plates"

    class Config:
        frozen = True


class GlobalConfig(BaseModel):
    projects_root: Path
    ocio_config: Path
    apps: Dict[str, str] = {}
    logs_dir: Path = Path.home() / ".xolo/logs"
    cache_dir: Path = Path.home() / ".xolo/cache"
    xolo_config_dir: Path = Path.home() / ".xolo/config"
