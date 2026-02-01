import typer
from core.xolo_core.api import scan_projects, scan_shots, set_globalconfig
from core.xolo_core.logging import events
app = typer.Typer(help="Create and manage projects")


@app.command()
def set():
    root_path = typer.prompt("Projects path")
    ocio_path = typer.prompt("OCIO path")
    nuke_path = typer.prompt("nuke path")
    gaffer_path = typer.prompt("gaffer path")
    blender_path = typer.prompt("blender path")
    projects_path = set_globalconfig(root=root_path, ocio=ocio_path, nuke=nuke_path, gaffer=gaffer_path, blender=blender_path)
