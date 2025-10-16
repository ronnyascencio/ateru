import typer


app = typer.Typer(help="Create and manage projects")


@app.command()
def create():
    typer.echo(
        "Creating a new project... (will create a new project folder pulled from templates)"
    )
