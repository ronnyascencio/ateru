from src.xolo.core.python.models.base import XoloBaseModel


class Asset(XoloBaseModel):
    sequence: str
    asset_name: str
    asset_type: str
    shot: str
    task: str
    work_dir: str
    publish_dir: str
    usd_stage_path: str
    frame_range: tuple[int, int]


class Shot(XoloBaseModel):
    sequence: str
    shot_name: str
    task: str
    work_dir: str
    publish_dir: str
    usd_stage_path: str
    frame_range: tuple[int, int]
