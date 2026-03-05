import typer

from typing import Annotated


app = typer.Typer()


@app.command()
def hello(
    name: str,
    upper_case: Annotated[bool, typer.Option(help="Change case to upper case.")] = False,
):
    if upper_case:
        name = name.upper()

    print(f"Hello {name}")
