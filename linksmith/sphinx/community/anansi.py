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
from copy import deepcopy
from functools import cache
from importlib.resources import files

import rich_click as click
import yaml
from pueblo.util.cli import boot_click
from verlib2 import Version

from linksmith.settings import help_config
from linksmith.sphinx.inventory import InventoryManager
from linksmith.sphinx.util import RemoteObjectsInv
from linksmith.util.data import multikeysort

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Item:
    """
    Manage an item in the project index file, e.g. `curated.yaml`.
    """

    name: str
    url: str
    version: t.Optional[Version] = None
    tags: t.Optional[t.List[str]] = dataclasses.field(default_factory=list)

    @classmethod
    def from_dict(cls, data: t.Dict):
        if "version" in data:
            data["version"] = Version(data["version"])
        return cls(**data)

    def to_dict(self):
        item = deepcopy(self)
        version = item.version
        if item.version:
            item.version = str(version)
        return dataclasses.asdict(item)


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
            data.append(Item.from_dict(raw))
        return multikeysort(data, "name", "-version")

    def to_list(self):
        """
        Convert list of items into vanilla list of Python dictionaries.
        """
        data = []
        for item in self.items:
            data.append(item.to_dict())
        return data

    def get_project_documentation_url(self, project: str) -> str:
        """
        Given a project name, attempt to resolve it via curated list, RTD, or PyPI.
        """
        logger.info(f"Attempting to resolve project from curated list: {project}")
        for item in self.items:
            if item.name == project:
                return item.url

        logger.info(f"Attempting to resolve project from Internet: {project}")
        try:
            return RemoteObjectsInv(project).discover()
        except FileNotFoundError as ex:
            logger.warning(ex)

        raise KeyError(f"Project not found: {project}")

    def suggest(self, project: str, term: str, threshold: int = 50) -> t.List[str]:
        """
        Find occurrences for "term" in Sphinx inventory.
        A wrapper around sphobjinv's `suggest`.

        `thresh` defines the minimum |fuzzywuzzy|_ match quality (an integer
        ranging from 0 to 100) required for a given object to be included in
        the results list. Can be any float value, but best results are generally
        obtained with values between 50 and 80.

        https://sphobjinv.readthedocs.io/en/stable/cli/suggest.html
        https://sphobjinv.readthedocs.io/en/stable/api/inventory.html#sphobjinv.inventory.Inventory.suggest
        """
        documentation_url = self.get_project_documentation_url(project)
        url = f"{documentation_url.rstrip('/')}/objects.inv"
        inv = InventoryManager(url).soi_factory()
        results = inv.suggest(term, thresh=threshold)
        if results:
            hits = len(results)
            logger.info(f"{hits} hits for project/term: {project}/{term}")
            return results
        else:
            logger.warning(f"No hits for project/term: {project}/{term}")
            return []


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
@click.pass_context
def cli_list_projects(ctx: click.Context):  # noqa: ARG001
    """
    List curated projects managed in accompanying `curated.yaml` file.
    """
    library = AnansiLibrary()
    results = library.to_list()
    print(yaml.dump(results))  # noqa: T201


@click.command()
@click.rich_config(help_config=help_config)
@click.argument("project")
@click.argument("term")
@click.option(
    "--threshold",
    type=int,
    default=50,
    required=False,
    help="Define the minimum fuzzywuzzy match quality (an integer ranging from 0 to 100) "
    "required for a given object to be included in the results list.",
)
@click.pass_context
def cli_suggest(ctx: click.Context, project: str, term: str, threshold: int = 50):  # noqa: ARG001
    """
    Fuzzy-search intersphinx inventory for desired object(s).
    """
    library = AnansiLibrary()
    try:
        results = library.suggest(project, term, threshold=threshold)
        print("\n".join(results))  # noqa: T201
    except (KeyError, FileNotFoundError) as ex:
        logger.error(str(ex).strip("'"))
        sys.exit(1)


cli.add_command(cli_list_projects, name="list-projects")
cli.add_command(cli_suggest, name="suggest")
