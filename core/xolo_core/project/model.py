from pydantic import BaseModel
from pathlib import Path
from typing import Tuple


class Xolo(BaseModel):
    projects_root: Path


class Project(BaseModel):
    id: int
    name: str
    root: Path
    fps: int
    resolution: Tuple[str, str]


class Shot(BaseModel):
    shot_name: str
    start: int
    end: int
    fps: int


class Asset(BaseModel):
    asset_type: str
    asset_name: str


class Publish(BaseModel):
    file_name: str
    work_file_version: str


class ProjectPaths:
    def __init__(self, root: Path):
        self.root = root
        self.config = root / "config" / "pconfig.toml"
        self.shots_root = root / "shots"
        self.assets_root = root / "assets"


class ShotPaths:
    def __init__(self, root: Path):
        self.root = root
        self.work = root / "work"
        self.publish = root / "publish"
        self.config = root / "sconfig.toml"


class AssetPaths:
    def __init__(self, root: Path):
        self.root = root
        self.work = root / "work"
        self.publish = root / "publish"
        self.config = root / "aconfig.toml"
