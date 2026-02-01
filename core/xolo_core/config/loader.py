try:
    import tomllib
except ImportError:
    import tomli as tomllib
from pathlib import Path

def read_xolo_config():
    config_file = Path.home() / ".xolo" / "xolo_config.toml"
    with open(config_file, "rb") as f:
        data = tomllib.load(f)
    projects_root: str = data["Paths"]["projects_root"]

    return Path(projects_root)


