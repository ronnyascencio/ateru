import typer
from xolo.core.api import set_software_paths, set_projects_root
from xolo.core.logging import events

app = typer.Typer(help="Create and manage projects")


@app.command()
def set():
    root_path = typer.prompt("Projects path")
    ocio_path = typer.prompt("OCIO path")
    nuke_path = typer.prompt("nuke path")
    gaffer_path = typer.prompt("gaffer path")
    blender_path = typer.prompt("blender path")
    projects_path = set_projects_root(root=root_path, ocio=ocio_path)
    software_path = set_software_paths(
        nuke=nuke_path, gaffer=gaffer_path, blender=blender_path
    )
