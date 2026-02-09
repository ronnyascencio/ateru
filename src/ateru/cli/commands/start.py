import typer
import subprocess
import sys
from ateru.ui.windows.show_manager import main as start_gui
from ateru.ui.windows.show_launcher import main as start_launcher
from ateru.core.logging import events

app = typer.Typer(help="start ateru app")


@app.command()
def manager():
    process = subprocess.Popen(
        [sys.executable, "src/ateru/ui/windows/show_manager.py"],
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
        [sys.executable, "ateru/ui/windows/show_launcher.py"],
        stdout=None,
        stderr=None,
    )

    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()