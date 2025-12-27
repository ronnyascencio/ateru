# core/xolo_core/context.py
from __future__ import annotations

import getpass
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field

from core.xolo_core.models.asset import Asset
from core.xolo_core.models.project import Project
from core.xolo_core.models.shot import Shot
from core.xolo_core.utils.logging import log_core


class Context(BaseModel):
    project: Project
    asset: Optional[Asset] = None
    shot: Optional[Shot] = None
    task: Optional[str] = None
    user: str = Field(default_factory=getpass.getuser)

    def get_env_map(self) -> dict[str, str]:
        """Genera el mapa de variables de entorno basado en los modelos."""

        envs = {
            "XOLO_PROJECT_NAME": str(self.project.name),
            "XOLO_PROJECT_ROOT": str(self.project.root_path),
            "XOLO_OCIO": str(self.project.ocio_path),
            "XOLO_USER": str(self.user),
            "XOLO_FPS": str(self.project.fps),  # Útil para que el DCC se configure solo
        }

        if self.asset:
            envs.update(
                {
                    "XOLO_CONTEXT_TYPE": "asset",
                    "XOLO_ASSET_NAME": str(self.asset.asset_name),
                    "XOLO_WORK_DIR": str(self.asset.work_dir),
                }
            )
        elif self.shot:
            envs.update(
                {
                    "XOLO_CONTEXT_TYPE": "shot",
                    "XOLO_SHOT_NAME": str(self.shot.shot_name),
                    "XOLO_SEQUENCE": str(self.shot.sequence),
                    "XOLO_WORK_DIR": str(self.shot.work_dir),
                }
            )

        if self.task:
            envs["XOLO_TASK"] = str(self.task)
        log_core(f"Generated environment variables: {envs}")

        return envs


class ContextResolver:
    @staticmethod
    def from_project_yaml(project_name: str, projects_root: Path) -> Context:
        yaml_path = projects_root / project_name / "config" / "project.yaml"

        if not yaml_path.exists():
            raise FileNotFoundError(f"No project.yaml in: {yaml_path}")

        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)

            project_model = Project(**data)

        return Context(project=project_model)
