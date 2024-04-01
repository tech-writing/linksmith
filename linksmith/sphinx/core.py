# ruff: noqa: T201 `print` found
import io
import logging
import typing as t
from pathlib import Path

import requests

from linksmith.model import OutputFormat, OutputFormatRegistry, ResourceType
from linksmith.sphinx.inventory import InventoryFormatter

logger = logging.getLogger(__name__)


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


def inventories_to_text(urls: t.Union[str, Path, io.IOBase], format_: str = "text"):
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
    if resource_type is ResourceType.BUFFER:
        url_list = t.cast(io.IOBase, urls).read().splitlines()
    elif resource_type is ResourceType.PATH:
        url_list = Path(t.cast(str, urls)).read_text().splitlines()
    # TODO: Test coverage needs to be unlocked by `test_multiple_inventories_url`
    elif resource_type is ResourceType.URL:  # pragma: nocover
        url_list = requests.get(t.cast(str, urls), timeout=10).text.splitlines()

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
