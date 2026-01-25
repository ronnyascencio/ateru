from pathlib import Path
import shutil
from core.xolo_core.shot.scan import list_shots
from core.xolo_core.config import loader
from core.xolo_core.logging import events


def shot_delete(shot_name: str, project_name: str):
    project_dir: Path = loader.read_xolo_config()
    shots_dir: Path = project_dir / project_name / "shots"
    shots: list = list_shots(shots_dir) or []

    if shot_name not in shots:
        events.error(f"Shot ->{shot_name}<- not found in Project: {project_name}")
        return
    try:
        shot_to_delete = project_dir / project_name / "shots" / shot_name

        shutil.rmtree(shot_to_delete)
        events.success(f"Shot: {shot_name}, deleted in root: {shot_to_delete}")
    except Exception as e:
        events.error(f"Could not delete {shot_name}: {str(e)}")
