import typer

from ateru.cli.commands import project, shot, scan, settings, start


app = typer.Typer(
    name="ateru", help="Open source VFX/Animation pipeline CLI.", no_args_is_help=True
)

app.add_typer(project.app, name="project")
app.add_typer(shot.app, name="shot")
app.add_typer(scan.app, name="scan")
app.add_typer(settings.app, name="settings")
app.add_typer(start.app, name="start")


if __name__ == "__main__":
    app(prog_name="ateru")
