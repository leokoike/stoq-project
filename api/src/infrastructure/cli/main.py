import typer
from src.infrastructure.cli.commands.seed import app as seed_app

app = typer.Typer(
    name="stoq-cli",
    help="Stoq API CLI - Database management and utilities",
)

app.add_typer(seed_app, name="seed")


if __name__ == "__main__":
    app()
