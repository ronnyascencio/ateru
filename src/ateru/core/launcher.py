import os
import subprocess
from pathlib import Path
from ateru.core.env.base import base_env
from ateru.core.env.nuke import nuke_env
from ateru.core.env.gaffer import gaffer_env
from ateru.core.env.blender import blender_env
from ateru.core.api import merge_pythonpath
import sys


def launch(dcc: str, executable: str, script: Path):
    """Lanza un DCC con su entorno y opcionalmente ejecuta un script bootstrap."""
    env = os.environ.copy()
    root = Path(__file__).resolve().parents[3]
    print(f"root is {root}")
    src = root / "src"
    print(f"src is {src}")
    vendor = src / "ateru" / "vendor"

    sep = os.pathsep

    # Base env
    base = base_env()
    merge_pythonpath(env, base["PYTHONPATH"])
    env.update({k: v for k, v in base.items() if k != "PYTHONPATH"})
    env["PYTHONPATH"] = f"{src}{sep}{vendor}" + sep + env.get("PYTHONPATH", "")

    # DCC env
    if dcc == "nuke":
        dcc_env = nuke_env()
        if "PYTHONPATH" in dcc_env:
            merge_pythonpath(env, dcc_env["PYTHONPATH"])
        env.update({k: v for k, v in dcc_env.items() if k != "PYTHONPATH"})
        cmd = [executable]
        if script:
            cmd += ["-t", str(script.resolve())]  # Nuke flag
    elif dcc == "blender":
        env.update(blender_env())
        cmd = [executable]
        if script:
            cmd += ["--python", str(script.resolve())]  # Blender flag
    elif dcc == "gaffer":
        dcc_env = gaffer_env()

        if "PYTHONPATH" in dcc_env:
            merge_pythonpath(env, dcc_env["PYTHONPATH"])

        env.update({k: v for k, v in dcc_env.items() if k != "PYTHONPATH"})

        # 👇 CREAR cmd AQUÍ
        cmd = [executable]

        # 👇 IMPORTANTE PARA GAFFER
        gaffer_startup = src / "ateru" / "integrations" / "gaffer" / "startup"

        env["GAFFER_STARTUP_PATHS"] = str(gaffer_startup)
        print(f"GAFFER_STARTUP_PATHS => {gaffer_startup}")

        print(f"env is {os.environ.get('GAFFER_STARTUP_PATH')}")

        if script:
            cmd += ["--script", str(script.resolve())]

    else:
        raise ValueError(f"DCC not supported: {dcc}")

    # Ejecutar DCC
    # En Linux y Windows funciona igual con subprocess
    subprocess.Popen(
        cmd, env=env, shell=(sys.platform == "win32"), start_new_session=True
    )
