"""CLI front-end"""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .parser import TfPlanParser

console = Console()


def main(
    input_file: Path = typer.Argument(..., exists=True, help="Terraform plan file"),
    json_out: bool = typer.Option(
        False, "--json", "-j", help="Emit JSON instead of a Rich table."
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="If set, writes JSON (with -j) or an HTML table here.",
    ),
) -> None:
    """Parse a Terraform plan and print a summary."""
    changes = TfPlanParser(input_file).parse()

    if json_out:
        payload = {act: dict(res) for act, res in changes.items()}
        text = json.dumps(payload, indent=2)
        console.print_json(text)
        if output:
            output.write_text(text, encoding="utf-8")
            console.print(f"[green]JSON saved to {output}")
    else:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Action")
        table.add_column("Resource type")
        table.add_column("Count", justify="right")

        for action, resources in changes.items():
            # sort by desc count
            for r_type, names in sorted(
                resources.items(), key=lambda item: len(item[1]), reverse=True
            ):
                table.add_row(action, r_type, str(len(names)))

        console.print(table)
        if output:
            console.save_html(str(output), inline_styles=True)
            console.print(f"[green]HTML saved to {output}")


# entry used by the console-script
def _entry() -> None:  # pragma: no cover
    typer.run(main)


if __name__ == "__main__":  # pragma: no cover
    _entry()
