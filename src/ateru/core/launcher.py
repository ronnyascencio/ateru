
import os
import subprocess
from pathlib import Path

from ateru.core.env.base import base_env
from ateru.core.env.nuke import nuke_env
from ateru.core.env.gaffer import gaffer_env
from ateru.core.env.blender import blender_env
from ateru.core.api import merge_pythonpath








def launch(dcc: str, executable: str):
    env = os.environ.copy()
    root = Path(__file__).resolve().parents[3]
    src = root / "src"
    vendor = src / "ateru" / "vendor"
    
    sep = os.pathsep
    

    base = base_env()
    merge_pythonpath(env, base["PYTHONPATH"])
    env.update({k: v for k, v in base.items() if k != "PYTHONPATH"})
    env["PYTHONPATH"] = f"{src}{sep}{vendor}" + sep + env.get("PYTHONPATH", "")

    if dcc == "nuke":
        dcc_env = nuke_env()
        if "PYTHONPATH" in dcc_env:
            merge_pythonpath(env, dcc_env["PYTHONPATH"])
        env.update({k: v for k, v in dcc_env.items() if k != "PYTHONPATH"})
    elif dcc == "gaffer":
        env.update(gaffer_env())
    elif dcc == "blender":
        env.update(blender_env())
    else:
        raise ValueError(f"DCC not supported: {dcc}")

    subprocess.Popen([executable], env=env)
