import os

from pathlib import Path

""" helper for set environmets """
def populate_environment():
    PIPELINE_ROOT = os.environ.get("PIPELINE_ROOT")
    if not PIPELINE_ROOT:
        raise EnvironmentError("PIPELINE_ROOT not defined")

    PIPELINE_ROOT = Path(PIPELINE_ROOT).resolve()

    CORE_PATH = PIPELINE_ROOT / "core"
    VENV_SITE = PIPELINE_ROOT / ".venv" / "lib" / "python3.11" / "site-packages"

    return {
        "PIPELINE_ROOT": str(PIPELINE_ROOT),
        "CORE_PATH": str(CORE_PATH),
        "VENV_SITE": str(VENV_SITE),
    }
