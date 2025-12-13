# ruff: noqa: T201 `print` found
import io
import logging
import typing as t
from pathlib import Path

import requests

from linksmith.model import OutputFormat, OutputFormatRegistry, ResourceType
from linksmith.sphinx.inventory import InventoryFormatter
from linksmith.sphinx.util import LocalConfPy, LocalObjectsInv, read_intersphinx_mapping_urls

logger = logging.getLogger(__name__)


def dump_inventory_universal(infiles: t.List[t.Any], format_: str = "text"):
    """
    Decode one or multiple intersphinx inventories and output in different formats.
    """
    if not infiles:
        logger.info("No inventory specified, entering auto-discovery mode")

        infiles = []
        try:
            local_objects_inv = LocalObjectsInv.discover(Path.cwd())
            logger.info(f"Auto-discovered objects.inv: {local_objects_inv}")
            infiles += [str(local_objects_inv)]
        except Exception as ex:
            logger.info(f"No inventory specified, and none discovered: {ex}")

        try:
            local_conf_py = LocalConfPy.discover(Path.cwd())
            logger.info(f"Auto-discovered conf.py: {local_conf_py}")
            intersphinx_urls = read_intersphinx_mapping_urls(local_conf_py)
            logger.info(f"Expanding infiles: {intersphinx_urls}")
            infiles += [intersphinx_urls]
        except Exception as ex:
            logger.info(f"No Sphinx project configuration specified, and none discovered: {ex}")

        if not infiles:
            raise FileNotFoundError("No inventory specified, and none discovered")

    # Pre-flight checks.
    for infile in infiles:
        ResourceType.detect(infile)

    # Process input files.
    for infile in infiles:
        if isinstance(infile, list) or infile.endswith(".txt"):
            inventories_to_text(infile, format_=format_)
        elif infile.endswith(".inv"):
            inventory_to_text(infile, format_=format_)
        else:
            raise NotImplementedError(f"Unknown input file type: {infile}")


def inventory_to_text(url: str, format_: str = "text"):
    """
    Display intersphinx inventory for individual project, using selected output format.
    """
    of = OutputFormatRegistry.resolve(format_)
    inventory = InventoryFormatter(url=url)

    if of is OutputFormat.TEXT_INSPECT:
        inventory.to_text_inspect()
    elif of is OutputFormat.TEXT_PLAIN:
        inventory.to_text_plain()
    elif of is OutputFormat.RESTRUCTUREDTEXT:
        inventory.to_restructuredtext()
    elif of in [OutputFormat.MARKDOWN, OutputFormat.MARKDOWN_TABLE]:
        inventory.to_markdown(format_)
    elif of is OutputFormat.HTML:
        inventory.to_html(format_)
    elif of is OutputFormat.JSON:
        inventory.to_json()
    elif of is OutputFormat.YAML:
        inventory.to_yaml()


def inventories_to_text(urls: t.Union[str, Path, io.IOBase, t.List], format_: str = "text"):
    """
    Display intersphinx inventories of multiple projects, using selected output format.
    """
    if format_.startswith("html"):
        print("<!DOCTYPE html>")
        print("<html>")
        print(
            """
        <style>
        html, body, table {
        font-size: small;
        }
        </style>
        """,
        )
        print("<body>")
    resource_type = ResourceType.detect(urls)
    url_list = []
    if resource_type is ResourceType.LIST:
        url_list = t.cast("list", urls)
    elif resource_type is ResourceType.BUFFER:
        url_list = t.cast("io.IOBase", urls).read().splitlines()
    elif resource_type is ResourceType.PATH:
        url_list = Path(t.cast("str", urls)).read_text().splitlines()
    elif resource_type is ResourceType.URL:
        url_list = requests.get(t.cast("str", urls), timeout=10).text.splitlines()

    # Generate header.
    if format_.startswith("html"):
        print("<h1>Inventory Overview</h1>")
        print(f"<p>Source: {urls}</p>")
        for url in url_list:
            inventory = InventoryFormatter(url=url)
            name = inventory.name
            print(f"""- <a href="#{name}">{name}</a><br/>""")

    # Generate content.
    for url in url_list:
        inventory_to_text(url, format_)
