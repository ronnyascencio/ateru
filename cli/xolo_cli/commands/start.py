import typer
import subprocess
import sys
from ui.show_manager import main as start_gui
from ui.show_launcher import main as start_launcher
from core.xolo_core.logging import events

app = typer.Typer(help="start xolo app")


@app.command()
def manager():
    process = subprocess.Popen(
        [sys.executable, "ui/show_manager.py"],
        stdout=None,
        stderr=None,
    )

    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()

@app.command()
def launcher():
    process = subprocess.Popen(
        [sys.executable, "ui/show_launcher.py"],
        stdout=None,
        stderr=None,
    )

    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()