from pathlib import Path

import yaml

from src.xolo.core.python.generators.variables_generator import ocio_variable
from src.xolo.core.python.models.base import XoloBaseModel
from src.xolo.core.python.models.project import Project
from src.xolo.core.python.utils.logging import log_core

""" global variables """


PIPELINE_ROOT: Path = Path(__file__).parent.parent.parent.parent.resolve()
CONFIG_PATH: Path = PIPELINE_ROOT / "pipeline_config.yaml"
STRUCTURE_PATH: Path = (
    PIPELINE_ROOT / "core" / "xolo_core" / "utils" / "project_structure.yml"
)


def load_config() -> dict[str, dict[str, str]]:
    """
    load config file from pipeline root preview set with
    xolo settings command
    """
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f) or {}

    return {}


def save_config(data):
    """save config file function"""
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def get_projects_root():
    """return project root loaded from config file"""
    projects_root = load_config()["global"]["projects_root"]
    return str(projects_root)


def create_project_directories(project: XoloBaseModel) -> None:
    """
    create project directories
    """
    yaml_path = Path(STRUCTURE_PATH).resolve()
    root_path = Path(get_projects_root())

    if not yaml_path.exists():
        raise FileNotFoundError(f"Structure file not found: {yaml_path}")

    with yaml_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    directories = data.get("directories", [])
    project_name = project.name

    project_root = root_path / project_name

    for directory in directories:
        path = project_root / directory
        path.mkdir(parents=True, exist_ok=True)
        log_core(f"Directory created: {path}")


def create_project_config(
    project_root: Path, name: str, resolution: tuple[int, int], fps: int
):
    """
    create project config file
    """
    user_resolution = resolution
    usd_path = project_root / "usd"
    OCIO_path = ocio_variable("Nuke")
    project = Project(
        name=name,
        fps=fps,
        resolution=user_resolution,
        usd_root=Path(usd_path).resolve(),
        ocio_path=str(OCIO_path),
        root_path=project_root,
        assets_path=project_root / "assets",
    )

    config_path = project_root / "config" / "project.yaml"
    config_path.write_text(
        yaml.safe_dump(project.model_dump(mode="json"), sort_keys=False)
    )


def load_project_config(project_root: Path) -> dict[str, object]:
    """
    load  Project config file from project root
    """
    project_root = Path(project_root).resolve()
    PROJECT_CONFIG = project_root / "config" / "project.yaml"
    if PROJECT_CONFIG.exists():
        with open(PROJECT_CONFIG, "r") as f:
            return yaml.safe_load(f) or {}

    return {}
