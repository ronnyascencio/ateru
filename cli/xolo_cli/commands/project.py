import typer
from core.xolo_core.api import create_project

app = typer.Typer(help="Create and manage projects")


@app.command()
def create():
    project_name = typer.prompt("project name")
    fps = typer.prompt("set fps")
    res_str = typer.prompt("Project Resolution (e.g. 1920x1080)")
    width, height = map(int, res_str.lower().replace(" ", "").split("x"))
    resolution = (width, height)
    res_w = str(width)
    res_h = str(height)

    project = create_project(
        project_name=project_name, fps=fps, width=res_w, height=res_h
    )
