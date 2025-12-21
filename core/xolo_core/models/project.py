from core.xolo_core.models.base import XoloBaseModel

class Project(XoloBaseModel):
    name: str
    fps: int
    resolution: tuple[int, int]
    usd_root: str
    OCIO_path: str
    root_path: str
