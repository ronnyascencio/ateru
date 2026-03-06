try:
    import tomllib
    import tomli_w
except ImportError:
    import tomli as tomllib
from pathlib import Path

CONFIG_FILE = Path.home() / ".ateru" / "ateru_config.toml"


def ensure_config_exists() -> dict:
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("rb") as f:
            return tomllib.load(f)
    else:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        base = {
            "title": {"name": "ateru Global Configuration"},
            "root": {"projects_root": str(Path.home() / "ateru_projects")},
            "apps": {},
        }
        with CONFIG_FILE.open("wb") as f:
            tomli_w.dump(base, f)
        return base


def read_ateru_config() -> Path:
    config = ensure_config_exists()
    root_path_str = config.get("root", {}).get("projects_root")
    if root_path_str:
        root_path = Path(root_path_str)
    else:
        root_path = Path.home() / "ateru_projects"

    root_path.mkdir(parents=True, exist_ok=True)

    return root_path


def read_ateru_config_apps(dcc: str) -> Path:
    config = ensure_config_exists()
    dcc_str = config.get("apps", {}).get(dcc)
    dcc_path = Path(dcc_str)

    return dcc_path
