from pydantic import BaseModel
from pathlib import Path
from typing import Tuple


class Xolo(BaseModel):
    projects_root: Path


class Project(BaseModel):
    id: int
    name: str
    root: Path
    renders: Path
    assets: Path
    plates: Path
    shots: Path
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
