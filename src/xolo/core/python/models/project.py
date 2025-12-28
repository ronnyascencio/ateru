from pathlib import Path

from src.xolo.core.python.models.base import XoloBaseModel


class Project(XoloBaseModel):
    name: str
    fps: int
    resolution: tuple[int, int]
    usd_root: Path
    ocio_path: str
    root_path: Path
    assets_path: Path
