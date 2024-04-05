"""
Curated intersphinx mappings by Brian Skinn, with a CLI.

Synopsis:

    anansi suggest matplotlib draw

Resources:
- https://github.com/bskinn/intersphinx-gist
- https://gist.github.com/bskinn/0e164963428d4b51017cebdb6cda5209
"""

import dataclasses
import logging
import sys
import typing as t
from functools import cache
from importlib.resources import files

import rich_click as click
import yaml
from pueblo.util.cli import boot_click

from linksmith.settings import help_config
from linksmith.sphinx.inventory import InventoryManager

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Item:
    """
    Manage an item in the project index file, e.g. `curated.yaml`.
    """

    name: str
    url: str
    version: t.Optional[str] = None
    tags: t.Optional[t.List[str]] = dataclasses.field(default_factory=list)


class AnansiLibrary:
    """
    Manage a list of curated projects, and provide exploration features on top of their Sphinx documentation.
    """

    index_file = "curated.yaml"

    @cache
    def read(self) -> t.List[Item]:
        return yaml.safe_load(files("linksmith.sphinx.community").joinpath(self.index_file).read_text())

    @property
    def items(self):
        data = []
        for raw in self.read():
            data.append(Item(**raw))
        return data

    def suggest(self, project: str, term: str):
        """
        Find occurrences for "term" in Sphinx inventory.
        A wrapper around sphobjinv's `suggest`.

        https://sphobjinv.readthedocs.io/en/stable/cli/suggest.html
        """
        for item in self.items:
            if item.name == project:
                url = f"{item.url.rstrip('/')}/objects.inv"
                inv = InventoryManager(url).soi_factory()
                results = inv.suggest(term)
                if results:
                    hits = len(results)
                    logger.info(f"{hits} hits for project/term: {project}/{term}")
                    return results
                else:
                    logger.warning(f"No hits for project/term: {project}/{term}")
                    return []
        else:
            raise KeyError(f"Project not found: {project}")


@click.group()
@click.rich_config(help_config=help_config)
@click.pass_context
def cli(ctx: click.Context):
    """
    Run operations on curated community projects.
    """
    if not ctx.parent:
        boot_click(ctx)


@click.command()
@click.rich_config(help_config=help_config)
@click.argument("project")
@click.argument("term")
@click.pass_context
def cli_suggest(ctx: click.Context, project: str, term: str):  # noqa: ARG001
    """
    Fuzzy-search intersphinx inventory for desired object(s).
    """
    library = AnansiLibrary()
    try:
        results = library.suggest(project, term)
        print("\n".join(results))  # noqa: T201
    except Exception as ex:
        logger.error(str(ex).strip("'"))
        sys.exit(1)


cli.add_command(cli_suggest, name="suggest")
