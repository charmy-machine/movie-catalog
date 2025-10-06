__all__ = ("app",)

import typer
from .tokens import app as tokens_app

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.callback()
def callback():
    """
    Some CLI management commands
    """


app.add_typer(tokens_app)
