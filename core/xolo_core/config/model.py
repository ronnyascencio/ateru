from pathlib import Path
from typing import Dict
from pydantic import BaseModel, Field


class ProjectConfig(BaseModel):
    root: Path

    assets_dir: str = "assets"
    shots_dir: str = "shots"
    renders_dir: str = "renders"
    config_dir: str = "config"
    editorial_dir: str = "editorial"
    plates_dir: str = "plates"

    model_config = {
        "frozen": True,
    }


class ShotConfig(BaseModel):
    root: Path

    work_dir: str = "work"
    publish_dir: str = "publish"

    model_config = {
        "frozen": True,
    }


class GlobalConfig(BaseModel):
    projects_root: Path
    ocio_config: Path

    apps: Dict[str, str] = Field(default_factory=dict)

    logs_dir: Path = Field(default_factory=lambda: Path.home() / ".xolo" / "logs")
    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".xolo" / "cache")
    xolo_config_dir: Path = Field(
        default_factory=lambda: Path.home() / ".xolo" / "config"
    )

    model_config = {
        "frozen": True,
    }
