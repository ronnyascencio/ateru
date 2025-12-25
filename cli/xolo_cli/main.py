import typer

from cli.xolo_cli.commands import launch, project, settings, version

app = typer.Typer()

app.add_typer(launch.app, name="launch")
app.add_typer(settings.app, name="settings")
app.add_typer(project.app, name="project")
app.add_typer(version.app, name="version")


if __name__ == "__main__":
    app()
