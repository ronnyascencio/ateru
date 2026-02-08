import typer
from ateru.core.api import scan_projects, scan_shots
from ateru.core.logging import events
app = typer.Typer(help="Create and manage projects")


@app.command()
def project():
    project = scan_projects()
    

@app.command()
def shot():
    project_name = typer.prompt("project name")
    shots = scan_shots(project_name=project_name)
