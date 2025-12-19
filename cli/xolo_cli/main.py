import typer

from cli.xolo_cli.commands import launch, project, settings
from core.xolo_core.utils.version_manager import (
    check_for_updates,
    get_version,
)

app = typer.Typer()

app.add_typer(launch.app, name="launch")
app.add_typer(settings.app, name="settings")
app.add_typer(project.app, name="project")


@app.command()
def version(
    refresh: bool = typer.Option(
        False, "--refresh", "-r", help="Force update from remote"
    ),
):
    """Show current installed version and check for updates."""
    current = get_version(force_refresh=refresh)
    typer.echo(f"📦 Xolo Pipeline version: {current}")

    latest = check_for_updates(current)
    if latest and latest != current:
        typer.echo(f"⚠️  A new version is available: {latest}")
    else:
        typer.echo("✅ You are using the latest version.")


if __name__ == "__main__":
    app()
