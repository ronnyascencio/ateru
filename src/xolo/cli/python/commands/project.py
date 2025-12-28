from pathlib import Path

import typer

from src.xolo.core.python.models.base import XoloBaseModel
from src.xolo.core.python.utils.format_show import format_project_info
from src.xolo.core.python.utils.logging import log_core
from src.xolo.core.python.utils.settings import (
    create_project_config,
    create_project_directories,
    get_projects_root,
    load_project_config,
)

app = typer.Typer(help="Create and manage projects")


@app.command()
def create() -> None:
    """Create a new project"""

    projects_root = Path(get_projects_root()).resolve()

    """
     validate project name
    """
    while True:
        try:
            project = typer.prompt("Project Name")
            base_model = XoloBaseModel(name=project)
            project_path = projects_root / project

            if project_path.exists():
                log_core(f"Project '{project}' already exists at {project_path}")
                log_core("Please choose another name.\n")
                continue

            break  # nombre válido y no existe

        except (typer.Abort, KeyboardInterrupt):
            log_core("Project creation aborted by user.")
            raise typer.Exit(code=1)

        except Exception as e:
            log_core(str(e))
            log_core("Invalid project name. Try again.\n")

    """ Validate resolution """
    while True:
        try:
            res_str = typer.prompt("Project Resolution (e.g. 1920x1080)")
            width, height = map(int, res_str.lower().replace(" ", "").split("x"))
            resolution = (width, height)
            break
        except (ValueError, typer.Abort, KeyboardInterrupt):
            log_core("Invalid resolution format. Use 1920x1080 or abort with Ctrl+C.")

    """ Validate fps"""
    while True:
        try:
            fps_map = int(typer.prompt("Project fps (e.g. 24)"))
            break
        except (ValueError, typer.Abort, KeyboardInterrupt):
            log_core("FPS must be a number or abort with Ctrl+C.")

    """ Create project directories and config """
    try:
        create_project_directories(project=base_model)

        project_root = projects_root / project

        create_project_config(
            project_root=project_root,
            name=project,
            resolution=resolution,
            fps=fps_map,
        )

        log_core(f"Project '{project}' created successfully")

    except Exception as e:
        log_core(f"Project creation failed: {e}")
        raise typer.Exit(code=1)


@app.command()
def show():
    project_root = get_projects_root()
    project = typer.prompt("Project Name")
    project_path = Path(project_root).resolve() / project
    if not project_path.exists():
        log_core(f"Project '{project}' does not exist at {project_path}")
        raise typer.Exit()
    else:
        info = load_project_config(project_root=project_path)
        info_formated = format_project_info(info)
        log_core(f"{info_formated}")


@app.command()
def delete():
    project = typer.prompt("Project Name")
    typer.echo(f"Deleting project: {project}")
