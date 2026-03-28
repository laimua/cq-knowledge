import typer
from typing import Optional

app = typer.Typer()

@app.command()
def test2(
    title: str = typer.Option(None, '--title', '-t', help='Title'),
):
    if title is None:
        raise typer.Exit('Title is required', code=1)
    print(f'Title: {title}')

if __name__ == '__main__':
    app()
