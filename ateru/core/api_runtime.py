# ateru/core/api_runtime.py
from typing import Optional
from pathlib import Path

from ateru.core import api
from ateru.core.dcc.base import DCCAdapterBase
from ateru.core.dcc.factory import detect_dcc


class XoloRuntime:
    def __init__(self):
        # -------- Context --------
        self.project: Optional[str] = None
        self.asset: Optional[str] = None
        self.shot: Optional[str] = None

        # -------- DCC --------
        self.dcc: Optional[DCCAdapterBase] = None

    # =====================================================
    # INIT
    # =====================================================
    def initialize(self):
        """Detect DCC automatically"""
        self.dcc = detect_dcc()

    # =====================================================
    # REQUIRE CONTEXT
    # =====================================================
    def require_project(self) -> str:
        if not self.project:
            raise RuntimeError("No project selected")
        return self.project

    def require_asset(self) -> str:
        if not self.asset:
            raise RuntimeError("No asset selected")
        return self.asset

    def require_shot(self) -> str:
        if not self.shot:
            raise RuntimeError("No shot selected")
        return self.shot

    # =====================================================
    # CONTEXT SETTERS
    # =====================================================
    def set_project(self, name: str):
        self.project = name
        self.asset = None
        self.shot = None

    def set_asset(self, name: str):
        self.asset = name
        self.shot = None

    def set_shot(self, name: str):
        self.shot = name

    # =====================================================
    # DOMAIN API
    # =====================================================
    def scan_projects(self):
        return api.scan_projects()

    def create_project(self, *args, **kwargs):
        return api.create_project(*args, **kwargs)

    def create_asset(self, asset_name: str, type: str):
        project = self.require_project()
        api.create_asset(
            project_name=project,
            asset_name=asset_name,
            type=type,
        )
        self.asset = asset_name

    # =====================================================
    # SCENE ACTIONS (GENERIC)
    # =====================================================
    def open_scene(self):
        self._ensure_dcc()
        path = self._resolve_scene_path()
        self.dcc.open_scene(path)

    def save_scene(self):
        self._ensure_dcc()
        path = self._resolve_scene_path()
        self.dcc.save_scene(path)

    # =====================================================
    # INTERNAL HELPERS
    # =====================================================
    def _ensure_dcc(self):
        if not self.dcc:
            raise RuntimeError("DCC not initialized")

    def _resolve_scene_path(self) -> Path:
        project = api.project_data(self.require_project())

        if self.asset:
            return (
                project.root
                / "assets"
                / self.asset
                / "work"
                / "scene"
            )

        if self.shot:
            return (
                project.root
                / "shots"
                / self.shot
                / "work"
                / "scene"
            )

        raise RuntimeError("No asset or shot selected")
