import typer

from core.actions import get_home_directory

app = typer.Typer(help="Create and manage projects")


@app.command()
def create(
    project: str = typer.Option(default="", help="Name of the project to create"),
):
    home_dir = get_home_directory().get("home")

    typer.echo(f"variables DEBUG: {home_dir}, {project}")
