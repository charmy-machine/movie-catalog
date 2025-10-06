from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens as tokens


app = typer.Typer(
    name="token",
    help="Tokens management",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(help="The token to check."),
    ],
) -> None:
    """Check if the passed token exists or not."""
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[green]exists[/green]."
            if tokens.token_exists(token)
            else "[red]does not exist[/red]."
        ),
    )


@app.command()
def create() -> None:
    """Create token."""
    token = tokens.generate_token_and_save()
    print(f"New token [bold]{token}[/bold] was generated and saved into storage.")


@app.command()
def add(
    token: Annotated[
        str,
        typer.Argument(help="The token to add."),
    ],
) -> None:
    """Add passed token to storage."""
    tokens.save_token(token)
    print(f"Token [bold]{token}[/bold] was saved into storage.")


@app.command(name="list")
def list_tokens() -> None:
    """List all tokens."""
    print(Markdown("# Available API Tokens"))
    print(Markdown("\n- ".join([""] + tokens.get_tokens())))
    print()


@app.command()
def rm(
    token: Annotated[
        str,
        typer.Argument(help="The token to delete."),
    ],
) -> None:
    """Delete the provided token from storage."""
    if not tokens.token_exists(token):
        print(f"Token [bold]{token}[/bold] [red]does not exist[/red].")
        return

    tokens.delete_token(token)
    print(f"[bold]{token}[/bold] was removed from DB.")
