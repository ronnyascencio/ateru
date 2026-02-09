import os
from ateru.core.logging import events
from pathlib import Path

from ateru.core.config import paths


def pieline_env():
    try:
        os.environ.clear()
        pip_dir: str = str(paths.pipeline_path())
        os.environ["PIPELINE_ROOT"] = pip_dir
        events.success("PIPELINE_ROOT env variable registered")
    except:
        events.error("PIPELINE_ROOT could not register env variable")
        

