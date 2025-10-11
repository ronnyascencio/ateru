import typer
from cli.commands import settings, launch

app = typer.Typer()

# Sub commands registred
app.add_typer(settings.app, name="settings")
app.add_typer(launch.app, name="launch")

if __name__ == "__main__":
    app()
