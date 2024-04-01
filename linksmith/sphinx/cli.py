import typing as t

import rich_click as click
from click import ClickException

from linksmith.settings import help_config
from linksmith.sphinx.core import inventories_to_text, inventory_to_text


@click.command()
@click.rich_config(help_config=help_config)
@click.argument("infiles", nargs=-1)
@click.option("--format", "format_", type=str, default="text", help="Output format")
@click.pass_context
def cli(ctx: click.Context, infiles: t.List[str], format_: str):
    """
    Decode one or multiple intersphinx inventories and output in different formats.

    Use `linksmith output-formats` to learn about available output formats.

    Examples:

    Refer to `objects.inv` on the local filesystem or on a remote location:
    ```bash
    linksmith inventory /path/to/objects.inv --format=html
    linksmith inventory https://linksmith.readthedocs.io/en/latest/objects.inv --format=markdown
    ```

    Refer to **multiple** `objects.inv` resources:
    ```bash
    linksmith inventory https://github.com/crate/crate-docs/raw/main/registry/sphinx-inventories.txt
    ```
    """
    if not infiles:
        raise click.ClickException("No input")
    for infile in infiles:
        try:
            if infile.endswith(".inv"):
                inventory_to_text(infile, format_=format_)
            elif infile.endswith(".txt"):
                inventories_to_text(infile, format_=format_)
            else:
                raise NotImplementedError(f"Unknown input file type: {infile}")
        except Exception as ex:
            if ctx.parent and ctx.parent.params.get("debug"):
                raise
            raise ClickException(f"{ex.__class__.__name__}: {ex}")
