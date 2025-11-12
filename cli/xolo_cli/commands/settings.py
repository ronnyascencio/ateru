from pathlib import Path

import typer
import yaml
from rich.console import Console

console = Console()

app = typer.Typer(help="Manage pipeline settings")

# Piepline root and pipeline_config.yaml
PIPELINE_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
CONFIG_PATH = PIPELINE_ROOT / "pipeline_config.yaml"


def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f) or {}
    return {}


def save_config(data):
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)


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
    Examble:
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
