import typer

from src.xolo.core.python.runtime import app_version
from src.xolo.core.python.updater.checker import has_update
from src.xolo.core.python.updater.installer import run_update

app = typer.Typer(help="Xolo version and updates")


@app.command()
def show():
    """Show current version"""
    typer.echo(f"Xolo Pipeline {app_version()}")


@app.command()
def check():
    """Check for updates"""
    update, latest = has_update()

    if not update:
        typer.echo("✔ Xolo Pipeline is up to date.")
        return

    typer.echo(f"⬆ New version available: {latest}")

    if typer.confirm("Do you want to update now?"):
        run_update()
