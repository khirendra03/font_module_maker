\"\"\"CLI wrapper for font_module_maker using Typer.
This module provides a simple `font-module-maker` CLI entry point that
calls the existing `make_module.main()` function for backward compatibility.
\"\"\"
import typer
import sys
from typing import Optional
import make_module

app = typer.Typer(add_completion=False)

@app.command()
def run(non_interactive: Optional[bool] = typer.Option(False, "--non-interactive", "-n", help="Run in non-interactive mode. Currently behaves the same as default and calls the original main().")):
    """
    Run the font module maker.
    """
    try:
        make_module.main()
    except SystemExit as e:
        raise typer.Exit(code=getattr(e, 'code', 1))
    except Exception as e:
        typer.secho(f\"Error: {e}\", err=True)
        raise typer.Exit(code=1)

if __name__ == '__main__':
    app()