from pathlib import Path
from typing import List
from core.xolo_core.config import loader


def list_assets(assets: Path) -> List[str] | None:
    """list projects names in the projects root directory"""
    assets: Path = assets

    assets_names = []

    for item in assets.iterdir():
        if item.is_dir():
            assets_names.append(item.name)
    return assets_names