import os
import subprocess
from pathlib import Path

import typer
from rich.console import Console

from core.xolo_core.generators.variables_generator import (
    ocio_variable,
    prman_variable,
    project_root_variable,
)

from .settings import load_config

app = typer.Typer(help="Launch DCCs")

console = Console()


@app.command()
def gaffer(project_name: str = typer.Argument(..., help="Project  base name.")):
    config = load_config()
    projects_root = config["global"]["projects_root"]
    project_path = Path(projects_root, project_name)
    project_root_variable(str(project_path))
    dcc_path = config["software"]["Gaffer"]["path"]
    console.print(f"DEBUG: DCC path  {dcc_path}", style="#F54927")
    if not dcc_path:
        typer.echo("❌ DCC 'Gaffer' not configurated.")
        raise typer.Exit(code=1)

    # Launch  DCC eredated env
    gaffer_path = Path(dcc_path, "gaffer").resolve()
    # 🔧 Asegurar entorno gráfico
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env.setdefault("DISPLAY", ":0")
    console.print(f"DEBUG: DCC path resolved  {gaffer_path}", style="#F54927")
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

    # Launch  DCC eredated env
    nuke_path = Path(dcc_path).resolve()
    console.rule("🚀 Launching Nuke...")
    subprocess.Popen([nuke_path, "--nukex"], env=os.environ)


@app.command()
def blender(
    project_name: str = typer.Argument(..., help="Project  base name."),
    render: str = typer.Option(None, help="Render engine to use."),
):
    config = load_config()
    projects_root = config["global"]["projects_root"]
    # TEMPLATE_DIR = f"{PIPELINE_ROOT}/dcc/blender/templates"
    # os.environ["XOLO_TEMPLATE_DIR"] = TEMPLATE_DIR
    project_path = Path(projects_root, project_name)
    # os.environ["BLENDER_USER_SCRIPTS"] = f"{PIPELINE_ROOT}/dcc/blender/addons"
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

    dcc_path = config["software"]["Blender"]["path"]
    console.print(f"DEBUG: DCC path  {dcc_path}", style="#F54927")
    if not dcc_path:
        typer.echo("❌ DCC 'Blender' not configurated.")
        raise typer.Exit(code=1)

    # Launch  DCC eredated env
    blender_path = Path(dcc_path).resolve()
    console.rule("🚀 Launching Blender...")
    subprocess.Popen([blender_path], env=os.environ)
