import typer

app = typer.Typer(help="Manage pipeline settings")


@app.command()
def show():
    """
    Show current pipeline configuration
    """
    typer.echo("Showing pipeline configuration... (will be load the config.yaml)")


@app.command()
def set(key: str, value: str):
    """
    Set a configuration key
    """
    typer.echo(f"Setting {key} = {value} in config.yaml")
