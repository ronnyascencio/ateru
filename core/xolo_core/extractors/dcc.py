import yaml
import os
import sys
from pathlib import Path

pipeline_root = os.getenv("PIPELINE_ROOT")
yaml_path = Path(str(pipeline_root))/ "core" / "xolo_core" / "utils" / "dcc_map.yml"

def load_map(dcc: str) -> list[str]:
    dcc = dcc.lower().strip()

    if not yaml_path.exists():
        raise FileNotFoundError(f"dcc_map.yml not found: {yaml_path}")

    with open(yaml_path, "r") as f:
        dcc_map = yaml.safe_load(f)

    software = dcc_map.get("software", {})

    if dcc not in software:
        raise ValueError(
            f"DCC not supported: '{dcc}'. Available: {list(software.keys())}"
        )

    return software[dcc].get("format", [])






def detect_dcc() -> str:
    exe = sys.executable.lower()

    if "blender" in exe:
        return "blender"
    if "nuke" in exe:
        return "nuke"
    if "gaffer" in exe:
        return "gaffer"

    return "standalone"
