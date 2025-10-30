from dataclasses import dataclass
from typing import Optional


""" Naming convention model"""


@dataclass
class WorkNaming:
    name: str
    task: str
    extention: Optional[str] = ""
    user_version: str = "u"
    version: Optional[int] = 1

    def get_versioned_name(self) -> str:
        """Generate the versioned name string."""
        return f"{self.name}_{self.task}_{self.user_version}{self.version:03d}.{self.extention}"


@dataclass
class PublishNaming:
    name: str
    task: str
    extention: str

    def get_publish_name(self) -> str:
        """Generate the publish name string."""
        return f"{self.name}_{self.task}.{self.extention}"
