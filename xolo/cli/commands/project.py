import typer
from xolo.core.api import create_project, delete_project
from xolo.core.logging import events

app = typer.Typer(help="Create and manage projects")


@app.command()
def create():
    project_name = typer.prompt("project name")
    type = typer.prompt("project type (e.g. animation, vfx)")
    fps = typer.prompt("set fps")
    res_str = typer.prompt("Project Resolution (e.g. 1920x1080)")
    width, height = map(int, res_str.lower().replace(" ", "").split("x"))
    res_w = str(width)
    res_h = str(height)

    project = create_project(
        project_name=project_name,
        fps=fps,
        width=res_w,
        height=res_h,
        type=type,
    )


@app.command()
def delete():
    project_name = typer.prompt("project name")
    _delete = typer.confirm(
        f"Are you sure you want to delete the project: {project_name}?", abort=True
    )
    if _delete:
        delete_project(project_name)
    else:
        events.error("Aborted")
