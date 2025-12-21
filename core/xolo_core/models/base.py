from pydantic import BaseModel
from pathlib import Path

class XoloBaseModel(BaseModel):
    name: str
    root: Path
