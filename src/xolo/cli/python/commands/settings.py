import typer
import yaml
from rich.console import Console

from src.xolo.core.python.utils.settings import load_config, save_config

console = Console()

app = typer.Typer(help="Manage pipeline settings")


@app.command()
def show():
    """
    Show current pipeline configuration
    """
    config = load_config()
    console.rule("[bold blue]Pipeline Configuration[/bold blue]")
    console.print(yaml.dump(config, sort_keys=False), style="blue", justify="left")


@app.command()
def set_projects(projects_root: str):
    """
    Set projects_root
    Example:
    set-projects "/home/projects"
    """
    config = load_config()

    # Config global
    config.setdefault("global", {})
    config["global"]["projects_root"] = projects_root
    save_config(config)
    console.print(
        f"projects_root {projects_root} configured in pipeline_ config.yaml!!",
        style="green",
    )


@app.command()
def set_dcc(software_name: str, software_version: str, software_path: str):
    """
    Set software configuration in one command.
    Example:
    set-dcc Nuke 14.0v3 "/usr/bin/nuke"
    """
    config = load_config()

    # Config software
    config.setdefault("software", {})
    config["software"].setdefault(software_name, {})
    config["software"][software_name]["version"] = software_version
    config["software"][software_name]["path"] = software_path

    save_config(config)
    console.print(
        f" {software_name} configured in pipeline_ config.yaml!", style="purple"
    )
