from pathlib import Path
import shutil
from core.xolo_core.project.scan import list_projects
from core.xolo_core.config import loader
from core.xolo_core.logging import events


def project_delete(project_name: str):
    project_dir: Path = loader.read_xolo_config()
    projects: list = list_projects(project_dir) or []

    if project_name not in projects:
        events.error(f"Project ->{project_name}<- not found in Projects")
        return
    try:
        project_to_delete = project_dir / project_name
        shutil.rmtree(project_to_delete)
        events.success(f"Project: {project_name}, deleted in root: {project_to_delete}")
    except Exception as e:
        events.error(f"Could not delete {project_name}: {str(e)}")
