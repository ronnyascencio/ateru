from pydantic import BaseModel
from pathlib import Path


class Asset(BaseModel):
    root: Path
    asset_type: str
    asset_name: str
