from core.xolo_core.models.base import XoloBaseModel

class Asset(XoloBaseModel):
    asset_name: str
    task: str
    work_dir: str
    publish_dir: str
    usd_stage_path: str
