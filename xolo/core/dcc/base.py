# core/xolo_core/dcc/base.py
from abc import ABC, abstractmethod
from pathlib import Path

class DCCAdapterBase(ABC):
    @abstractmethod
    def load_usd(self, path: Path):
        pass

    @abstractmethod
    def save_usd(self, path: Path):
        pass

    @abstractmethod
    def open_scene(self, path: Path):
        pass

    @abstractmethod
    def save_scene(self, path: Path):
        pass
