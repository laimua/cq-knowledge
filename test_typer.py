import typer

app = typer.Typer()

@app.command()
def test(
    title: str = typer.Option(..., '--title', '-t', help='Title'),
):
    print(f'Title: {title}')

if __name__ == '__main__':
    app()
