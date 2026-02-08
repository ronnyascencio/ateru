from typing import Tuple
from pydantic import BaseModel
from pathlib import Path
from ateru.core.config.model import Xolo
from ateru.core.project.model import Project
from ateru.core.config.paths import (
    resolve_project_paths,
    resolve_xolo_path,
    resolve_shot_path,
    resolve_asset_path,
)
from ateru.core.config.model import AssetConfig
from ateru.core.logging import events
from ateru.core.config.loader import read_xolo_config
from ateru.core.project.load import read_project_config
import uuid
import tomli_w


"""
core creation for shots


"""


def create_asset_structure(project_name: str, asset_name: str):
    project_config = read_project_config(project_name)
    root_assets = project_config.root / project_config.assets_dir / asset_name

    model = AssetConfig(root=root_assets)

    directories = resolve_asset_path(model)

    for path in directories.values():
        path.mkdir(parents=True, exist_ok=True)
        events.info(f"Created directory: {path}")
