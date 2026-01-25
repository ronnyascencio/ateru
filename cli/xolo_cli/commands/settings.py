import typer
from core.xolo_core.api import scan_projects, scan_shots, set_globalconfig
from core.xolo_core.logging import events
app = typer.Typer(help="Create and manage projects")


@app.command()
def set():
    root_path = typer.prompt("Projects path")
    projects_path = set_globalconfig(root=root_path)
    

