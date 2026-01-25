import typer

from cli.xolo_cli.commands import project, shot, scan, settings


app = typer.Typer()

app.add_typer(project.app, name="project")
app.add_typer(shot.app, name="shot")
app.add_typer(scan.app, name="scan")
app.add_typer(settings.app, name="settings")
# app.add_typer(version.app, name="version")


if __name__ == "__main__":
    app()
