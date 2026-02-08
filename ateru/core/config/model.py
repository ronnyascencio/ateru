from pathlib import Path
from typing import Dict, Annotated, Optional
from pydantic import BaseModel, Field, field_validator

import re


class Xolo(BaseModel):
    projects_root: Path


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


class AssetConfig(BaseModel):
    root: Path

    type: str | None = None
    work_dir: str = "work"
    publish_dir: str = "publish"

    model_config = {
        "frozen": True,
    }


class GlobalConfig(BaseModel):
    projects_root: Path
    ocio_config: Optional[Path]



    logs_dir: Path = Field(default_factory=lambda: Path.home() / ".ateru" / "logs")
    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".ateru" / "cache")


    model_config = {
        "frozen": True,
    }

class SoftwareConfig(BaseModel):
    nuke_path: Path
    gaffer_path: Path
    blender_path: Path


class Version(BaseModel):
    value: str = "v000"

    @field_validator("value")
    @classmethod
    def validate_version(cls, v: str) -> str:
        if not re.fullmatch(r"v\d{3}", v):
            raise ValueError("Version must match format v000")
        return v

    @property
    def number(self) -> int:
        """v012 -> 12"""
        return int(self.value[1:])

    def bump(self, step: int = 1) -> "Version":
        new_number = self.number + step
        return Version(value=f"v{new_number:03d}")


class NamingConvention(BaseModel):
    name: str
    task: str
    version: Version = Field(default_factory=Version)

    def bump_version(self, step: int = 1) -> "NamingConvention":
        return self.model_copy(update={"version": self.version.bump(step)})

    def __str__(self) -> str:
        return f"{self.name}_{self.task.upper()}_{self.version.value}"


class Publish(BaseModel):
    file_name: str
    publish_root: Path
    work_file_version: str
    work_root: Path
