import typer
import os
import subprocess
from pathlib import Path
from core.xolo_core.generators.variables_generator import project_root_variable
from core.xolo_core.generators.dcc_generator import dcc_root_path


app = typer.Typer(help="Launch DCCs or pipeline tasks")


@app.command()
def gaffer():
    typer.echo(
        "Launching Gaffer... (here will be integrate with tu folder /dcc/gaffer)"
    )


@app.command()
def nuke(project_root: str = typer.Argument(..., help="Path base de proyectos.")):
    project_path = project_root_variable(
        project_root,
    )
    typer.echo(f"PROJECT_ROOT set to: {project_path}")
    dcc_path = dcc_root_path("nuke")
    print(f"Debug dcc path: {dcc_path}")
    if not dcc_path:
        typer.echo("❌ DCC 'Nuke' no está configurado.")
        raise typer.Exit(code=1)

    # Launch  DCC eredated env
    nuke_path = Path(dcc_path, "Nuke16.0").resolve()
    typer.echo("🚀 Launching Nuke...")
    subprocess.Popen([nuke_path, "--nukex"], env=os.environ)
    typer.echo("Launching Nuke... (here will be integrate with /dcc/nuke)")


@app.command()
def blender():
    typer.echo("Launching Blender... (here will be integrate with /dcc/blender)")
