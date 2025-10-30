import typer
from cli.xolo_cli.commands import settings, launch, project
import requests
import importlib.metadata

app = typer.Typer()

# Sub commands registred
app.add_typer(settings.app, name="settings")
app.add_typer(launch.app, name="launch")
app.add_typer(project.app, name="project")
# app.add_typer(version.app, name="version")


GITHUB_API_URL = "https://api.github.com/xololab/xolo-pipeline/releases/tags/lastest"


def get_local_version() -> str:
    try:
        return importlib.metadata.version("xolo-pipeline")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def get_remote_version() -> None:
    """Obtiene la última versión publicada en GitHub."""
    try:
        payload = dict(key1="value1", key2="value2")
        response = requests.get(GITHUB_API_URL, data=payload)
        # response.raise_for_status()
        # data = response.json()
        return print(response.text)  # data.get("tag_name", "unknown")
    except Exception:
        return  # "unknown"


@app.command()
def version(
    remote: bool = typer.Option(
        False, "--remote", "-r", help="Fetch version from GitHub"
    ),
):
    """Muestra la versión del pipeline."""
    local = get_local_version()
    typer.echo(f"Local version: {local}")

    if remote:
        remote_ver = get_remote_version()
        typer.echo(f"Latest GitHub release: {remote_ver}")
        if remote_ver != "unknown" and remote_ver != local:
            typer.echo(f"⚠️  Your version is out of date (latest is {remote_ver}).")


if __name__ == "__main__":
    app()
