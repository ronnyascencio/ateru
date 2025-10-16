import typer

app = typer.Typer(help="Launch DCCs or pipeline tasks")


@app.command()
def gaffer():
    typer.echo(
        "Launching Gaffer... (here will be integrate with tu folder /dcc/gaffer)"
    )


@app.command()
def nuke():
    typer.echo("Launching Nuke... (here will be integrate with /dcc/nuke)")


@app.command()
def blender():
    typer.echo("Launching Blender... (here will be integrate with /dcc/blender)")
