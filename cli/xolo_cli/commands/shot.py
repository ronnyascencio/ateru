import typer
from core.xolo_core.api import create_shot, delete_shot
from core.xolo_core.logging import events

app = typer.Typer(help="Create and manage shots")


@app.command()
def create():
    project_name = typer.prompt("project name")
    shot_name = typer.prompt("shot name (e.g. '000_010'")
    fps = typer.prompt("set fps")
    res_str = typer.prompt("frame range (e.g. 1001-1100)")
    start, end = map(int, res_str.lower().replace(" ", "").split("-"))
    f_start = start
    f_end = end

    project = create_shot(
        shot_name=shot_name,
        project_name=project_name,
        fps=fps,
        start=f_start,
        end=f_end,
    )


@app.command()
def delete():
    project_name = typer.prompt("project name")
    shot_name = typer.prompt("shot name (e.g. '000_010'")
    _delete = typer.confirm(
        f"Are you sure you want to delete the shot: {shot_name}?", abort=True
    )
    if _delete:
        delete_shot(project_name, shot_name)
    else:
        events.error("Aborted")
