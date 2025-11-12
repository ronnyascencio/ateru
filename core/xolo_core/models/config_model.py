from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ProjectConfig:
    project_root: str
    project_name: str
    project_type: str
    status: str = "new"
    client_name: Optional[str] = None
    fps: int
    resolution: List[str] = field(default_factory=lambda: ["1920", "1080"])
