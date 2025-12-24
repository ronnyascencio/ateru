from pathlib import Path

from core.xolo_core.models.base import XoloBaseModel


class Project(XoloBaseModel):
    name: str
    fps: int
    resolution: tuple[int, int]
    usd_root: Path
    ocio_path: str
    root_path: Path
    assets_path: Path
