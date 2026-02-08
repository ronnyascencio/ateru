from pathlib import Path
from typing import List
from ateru.core.config import loader


def list_shots(shots: Path) -> List[str] | None:
    """list projects names in the projects root directory"""
    shots: Path = shots

    shots_names = []

    for item in shots.iterdir():
        if item.is_dir():
            shots_names.append(item.name)
    return shots_names