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






