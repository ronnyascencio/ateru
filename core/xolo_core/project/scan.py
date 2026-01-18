from pathlib import Path
from typing import List
from core.xolo_core.config import loader


def list_projects(projects: Path) -> List[str] | None:
    """list projects names in the projects root directory"""
    projects: Path = projects

    projects_names = []

    for item in projects.iterdir():
        if item.is_dir():
            projects_names.append(item.name)
    return projects_names
    

