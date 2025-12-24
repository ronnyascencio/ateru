import os
import subprocess
from pathlib import Path

import typer
from rich.console import Console

from core.xolo_core.generators.declare_generator import populate_environment
from core.xolo_core.generators.variables_generator import (
    core_path,
    ocio_variable,
    prman_variable,
    project_root_variable,
)
from core.xolo_core.utils.settings import load_config

app = typer.Typer(help="Launch DCCs")

console = Console()


PIPELINE_ROOT, CORE_PATH, VENV_SITE = populate_environment()


@app.command()
def gaffer(project_name: str = typer.Argument(..., help="Project base name.")):
    config = load_config()
    projects_root = config["global"]["projects_root"]
    project_path = Path(projects_root, project_name)

    dcc_path = config["software"]["Gaffer"]["path"]

    gaffer_path = Path(dcc_path, "gaffer").resolve()

    # startup root path
    custom_root = Path(core_path()).resolve() / "dcc" / "gaffer" / "startup"

    # env context
    env = os.environ.copy()
    _ = env.pop("PYTHONPATH", None)
    _ = env.pop("PYTHONHOME", None)
    env.setdefault("DISPLAY", ":0")

    # PROJECT_ROOT variable inyection
    env["PROJECT_ROOT"] = str(project_path)

    #  Setiing up gaffer start up variable
    env["GAFFER_STARTUP_PATHS"] = str(custom_root)
    env["PYTHONPATH"] = str(os.environ.get("PIPELINE_ROOT"))

    console.print(f"DEBUG: Startup Path: {custom_root}", style="green")
    console.print(f"DEBUG: Project Root: {env['PROJECT_ROOT']}", style="green")

    # Launch  DCC eredated env
    console.rule("🚀 Launching Gaffer...")
    proc = subprocess.Popen([str(gaffer_path)], env=env, start_new_session=True)
    print(f"Launched Gaffer with PID {proc.pid}")


@app.command()
def nuke(project_name: str = typer.Argument(..., help="Project base name.")):
    config = load_config()
    projects_root = config["global"]["projects_root"]
    project_path = Path(projects_root, project_name)

    ocio_variable("Nuke")
    project_root_variable(str(project_path))
    dcc_path = config["software"]["Nuke"]["path"]
    console.print(f"DEBUG: DCC path  {dcc_path}", style="yellow")
    if not dcc_path:
        typer.echo("❌ DCC 'Nuke' no configurated.")
        raise typer.Exit(code=1)

    # env context
    env = os.environ.copy()
    _ = env.pop("PYTHONPATH", None)
    _ = env.pop("PYTHONHOME", None)
    env["PROJECT_ROOT"] = str(project_path)
    env["NUKE_PATH"] = os.pathsep.join(
        [
            str(Path(PIPELINE_ROOT) / "dcc" / "nuke"),
            str(CORE_PATH),
        ]
    )

    env["PYTHONPATH"] = os.pathsep.join(
        [
            str(CORE_PATH),
            str(Path(PIPELINE_ROOT) / ".venv" / "lib" / "python3.11" / "site-packages"),
            env.get("PYTHONPATH", ""),
        ]
    )

    # Launch  DCC eredated env
    nuke_path = Path(dcc_path).resolve()
    console.rule("🚀 Launching Nuke...")
    subprocess.Popen([nuke_path, "--nukex", "--nc"], env=env)


@app.command()
def blender(
    project_name: str = typer.Argument(..., help="Project  base name."),
    render: str = typer.Option(None, help="Render engine to use."),
):
    config = load_config()
    projects_root = config["global"]["projects_root"]
    project_path = Path(projects_root, project_name)
    project_root_variable(str(project_path))
    if render == "pixar":
        ocio_file = "lib/ocio/ACES-1.3/config.ocio"

        opt = prman_variable()
        ocio_env = Path(opt, ocio_file).resolve()
        os.environ["OCIO"] = str(ocio_env)
        os.environ["RMANTREE"] = str(opt)
        console.print(f"DEBUG: Pixar OCIO  {os.environ.get('OCIO')}", style="blue")
        console.print(
            f"DEBUG: Pixar RMANTREE  {os.environ.get('RMANTREE')}", style="blue"
        )

    else:
        ocio_variable("Blender")

    blender_scripts_path = (
        Path(__file__).parent.parent.parent.parent / "dcc" / "blender" / "scripts"
    )

    # env context
    env = os.environ.copy()
    _ = env.pop("PYTHONPATH", None)
    _ = env.pop("PYTHONHOME", None)

    env["BLENDER_USER_SCRIPTS"] = str(blender_scripts_path)
    env["OCIO"] = os.environ.get("OCIO", "")

    dcc_path = config["software"]["Blender"]["path"]
    if not dcc_path:
        typer.echo("❌ DCC 'Blender' not configurated.")
        raise typer.Exit(code=1)

    blender_path = Path(dcc_path).resolve()
    console.rule("🚀 Launching Blender...")

    # Force Blender to activate addons
    cmd = [
        str(blender_path),
        "--python-expr",
        (
            "import sys, os;"
            "root=os.environ['PIPELINE_ROOT'];"
            "sys.path.insert(0, root);"
            "sys.path.insert(0, os.path.join(root, 'core'));"
            "sys.path.insert(0, os.path.join(root, '.venv', 'lib', 'python3.11', 'site-packages'));"
        ),
        "--addons",
        "xolo_tools",
    ]

    subprocess.Popen(cmd, env=env)
