import typer
from xolo.core.api import scan_projects, scan_shots
from xolo.core.logging import events
app = typer.Typer(help="Create and manage projects")


@app.command()
def project():
    project = scan_projects()
    

@app.command()
def shot():
    project_name = typer.prompt("project name")
    shots = scan_shots(project_name=project_name)
