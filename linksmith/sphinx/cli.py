import logging
import typing as t

import rich_click as click

from linksmith.settings import help_config
from linksmith.sphinx.core import dump_inventory_universal

logger = logging.getLogger(__name__)


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

    Discover `objects.inv` in working directory:
    ```bash
    linksmith inventory
    ```
    """
    try:
        dump_inventory_universal(infiles, format_)
    except Exception as ex:
        if ctx.parent and ctx.parent.params.get("debug"):
            raise
        raise click.ClickException(str(ex))
