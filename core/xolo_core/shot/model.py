from pydantic import BaseModel
from pathlib import Path


class Shot(BaseModel):
    root: Path
    shot_name: str
    start: int
    end: int
    fps: int
