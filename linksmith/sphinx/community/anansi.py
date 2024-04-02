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

import rich_click as click
from pueblo.util.cli import boot_click

from linksmith.settings import help_config
from linksmith.sphinx.inventory import InventoryManager

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Item:
    name: str
    url: str


items = [
    Item("python@3", "https://docs.python.org/3/"),
    Item("python@3.9", "https://docs.python.org/3.9/"),
    Item("attrs", "https://www.attrs.org/en/stable/"),
    Item("django", "https://docs.djangoproject.com/en/dev/"),
    Item("flask@2.2", "https://flask.palletsprojects.com/en/2.2.x/"),
    Item("flask@1.1", "https://flask.palletsprojects.com/en/1.1.x/"),
    Item("h5py", "https://docs.h5py.org/en/latest/"),
    Item("matplotlib", "https://matplotlib.org/stable/"),
    Item("numpy", "https://numpy.org/doc/stable/"),
    Item("pandas", "https://pandas.pydata.org/docs/"),
    Item("pyramid", "https://docs.pylonsproject.org/projects/pyramid/en/latest/"),
    Item("scikit-learn", "https://scikit-learn.org/stable/"),
    Item("sphinx", "https://www.sphinx-doc.org/en/master/"),
    Item("sympy", "https://docs.sympy.org/latest/"),
    Item("scipy", "https://docs.scipy.org/doc/scipy/"),
    Item("scipy@1.8.1", "https://docs.scipy.org/doc/scipy-1.8.1/"),
    Item("scipy@1.8.0", "https://docs.scipy.org/doc/scipy-1.8.0/"),
    Item("scipy@1.7.1", "https://docs.scipy.org/doc/scipy-1.7.1/"),
    Item("scipy@1.7.0", "https://docs.scipy.org/doc/scipy-1.7.0/"),
    Item("scipy@1.6.3", "https://docs.scipy.org/doc/scipy-1.6.3/reference/"),
    Item("sarge", "https://sarge.readthedocs.io/en/latest/"),
]


def suggest(project: str, term: str):
    for item in items:
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
    try:
        results = suggest(project, term)
        print("\n".join(results))  # noqa: T201
    except Exception as ex:
        logger.error(str(ex).strip("'"))
        sys.exit(1)


cli.add_command(cli_suggest, name="suggest")
