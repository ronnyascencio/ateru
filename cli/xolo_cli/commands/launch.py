import os
import subprocess
from pathlib import Path

import typer
from rich.console import Console

from core.xolo_core.generators.variables_generator import (
    core_path,
    ocio_variable,
    prman_variable,
    project_root_variable,
)

from .settings import load_config

app = typer.Typer(help="Launch DCCs")

console = Console()


@app.command()
def gaffer(project_name: str = typer.Argument(..., help="Project base name.")):
    config = load_config()
    projects_root = config["global"]["projects_root"]
    project_path = Path(projects_root, project_name)

    dcc_path = config["software"]["Gaffer"]["path"]

    gaffer_path = Path(dcc_path, "gaffer").resolve()

    # startup root path
    custom_root = Path(core_path()).resolve() / "dcc" / "gaffer" / "startup"

    # env context
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env.setdefault("DISPLAY", ":0")

    # PROJECT_ROOT variable inyection
    env["PROJECT_ROOT"] = str(project_path)

    #  Setiing up gaffer start up variable
    env["GAFFER_STARTUP_PATHS"] = str(custom_root)

    console.print(f"DEBUG: Startup Path: {custom_root}", style="green")
    console.print(f"DEBUG: Project Root: {env['PROJECT_ROOT']}", style="green")

    # Launch  DCC eredated env
    console.rule("🚀 Launching Gaffer...")
    proc = subprocess.Popen([str(gaffer_path)], env=env, start_new_session=True)
    print(f"Launched Gaffer with PID {proc.pid}")


@app.command()
def nuke(project_name: str = typer.Argument(..., help="Project base name.")):
    config = load_config()
    projects_root = config["global"]["projects_root"]
    project_path = Path(projects_root, project_name)

    ocio_variable("Nuke")
    project_root_variable(str(project_path))
    dcc_path = config["software"]["Nuke"]["path"]
    console.print(f"DEBUG: DCC path  {dcc_path}", style="yellow")
    if not dcc_path:
        typer.echo("❌ DCC 'Nuke' no configurated.")
        raise typer.Exit(code=1)

    # env context
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)

    # Launch  DCC eredated env
    nuke_path = Path(dcc_path).resolve()
    console.rule("🚀 Launching Nuke...")
    subprocess.Popen([nuke_path, "--nukex"], env=env)


@app.command()
def blender(
    project_name: str = typer.Argument(..., help="Project  base name."),
    render: str = typer.Option(None, help="Render engine to use."),
):
    config = load_config()
    projects_root = config["global"]["projects_root"]
    project_path = Path(projects_root, project_name)
    project_root_variable(str(project_path))
    if render == "pixar":
        ocio_file = "lib/ocio/ACES-1.3/config.ocio"

        opt = prman_variable()
        ocio_env = Path(opt, ocio_file).resolve()
        os.environ["OCIO"] = str(ocio_env)
        os.environ["RMANTREE"] = str(opt)
        console.print(f"DEBUG: Pixar OCIO  {os.environ.get('OCIO')}", style="blue")
        console.print(
            f"DEBUG: Pixar RMANTREE  {os.environ.get('RMANTREE')}", style="blue"
        )

    else:
        ocio_variable("Blender")

    blender_scripts_path = (
        Path(__file__).parent.parent.parent.parent / "dcc" / "blender" / "scripts"
    )

    # 2. Preparar el entorno LIMPIO
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)  # Importante: Limpiar para evitar conflictos de Python
    env.pop("PYTHONHOME", None)

    # Agregar variables ESPECÍFICAS al entorno limpio
    env["BLENDER_USER_SCRIPTS"] = str(blender_scripts_path)
    env["OCIO"] = os.environ.get("OCIO", "")  # Asegurar que OCIO pase si existe

    # Contexto del Pipeline (XOLO_PROJECT, etc. ya deben estar seteados antes o aquí)
    # env["XOLO_PROJECT"] = project_name

    dcc_path = config["software"]["Blender"]["path"]
    if not dcc_path:
        typer.echo("❌ DCC 'Blender' not configurated.")
        raise typer.Exit(code=1)

    blender_path = Path(dcc_path).resolve()
    console.rule("🚀 Launching Blender...")

    # 3. Comando de lanzamiento con AUTO-ACTIVACIÓN del addon
    # Esto fuerza a Blender a activar 'xolo_tools' al iniciar
    cmd = [
        str(blender_path),
        "--python-expr",
        "import bpy; bpy.ops.preferences.addon_enable(module='xolo_tools')",
    ]

    subprocess.Popen(cmd, env=env)
