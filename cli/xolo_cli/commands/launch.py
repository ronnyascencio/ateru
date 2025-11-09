import os
import subprocess
from pathlib import Path

import typer
from rich.console import Console

from core.xolo_core.generators.variables_generator import (
    ocio_variable,
    project_root_variable,
)

from .settings import load_config

app = typer.Typer(help="Launch DCCs")

console = Console()


@app.command()
def gaffer():
    typer.echo(
        "Launching Gaffer... (here will be integrate with tu folder /dcc/gaffer)"
    )


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
def blender(project_name: str = typer.Argument(..., help="Project  base name.")):
    config = load_config()
    projects_root = config["global"]["projects_root"]
    project_path = Path(projects_root, project_name)
    ocio_variable("Blender")
    project_root_variable(str(project_path))
    dcc_path = config["software"]["Blender"]["path"]
    console.print(f"DEBUG: DCC path  {dcc_path}", style="#F54927")
    if not dcc_path:
        typer.echo("❌ DCC 'Blender' not configurated.")
        raise typer.Exit(code=1)

    # Launch  DCC eredated env
    blender_path = Path(dcc_path).resolve()
    console.rule("🚀 Launching Blender...")
    subprocess.Popen([blender_path], env=os.environ)
