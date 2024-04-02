import json

import rich_click as click
from pueblo.util.cli import boot_click

from linksmith.settings import help_config

from .model import OutputFormatRegistry
from .sphinx.cli import cli as inventory_cli
from .sphinx.community.anansi import cli as anansi_cli


@click.group()
@click.rich_config(help_config=help_config)
@click.option("--verbose", is_flag=True, required=False, help="Turn on logging")
@click.option("--debug", is_flag=True, required=False, help="Turn on logging with debug level")
@click.version_option()
@click.pass_context
def cli(ctx: click.Context, verbose: bool, debug: bool):
    return boot_click(ctx, verbose, debug)


@click.command()
@click.rich_config(help_config=help_config)
@click.pass_context
def output_formats(ctx: click.Context):  # noqa: ARG001
    """
    Display available output format aliases.
    """
    print(json.dumps(sorted(OutputFormatRegistry.aliases()), indent=2))


cli.add_command(output_formats, name="output-formats")
cli.add_command(inventory_cli, name="inventory")
cli.add_command(anansi_cli, name="anansi")
