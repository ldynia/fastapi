import typer

from cli.hello import app as hello
from cli.goodbye import app as goodbye


app = typer.Typer()

app.add_typer(hello)
app.add_typer(goodbye)


if __name__ == "__main__":
    app()
