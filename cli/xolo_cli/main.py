import typer
from cli.xolo_cli.commands import settings, launch, project

app = typer.Typer()

# Sub commands registred
app.add_typer(settings.app, name="settings")
app.add_typer(launch.app, name="launch")
app.add_typer(project.app, name="project")

if __name__ == "__main__":
    app()
