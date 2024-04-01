"""
Format content of Sphinx inventories.

Source:
- https://github.com/crate/crate-docs/blob/5a7b02f/tasks.py
- https://github.com/pyveci/pueblo/blob/878a31f94/pueblo/sphinx/inventory.py
"""

import dataclasses
import io
import logging
import typing as t
from contextlib import redirect_stdout

import sphobjinv as soi
import tabulate
import yaml
from marko.ext.gfm import gfm as markdown_to_html
from sphinx.application import Sphinx
from sphinx.ext.intersphinx import fetch_inventory, inspect_main
from sphinx.util.typing import InventoryItem

from linksmith.model import ResourceType

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class InventoryRecord:
    """
    Manage details of a single record of a Sphinx inventory.
    """

    type: str
    name: str
    project: str
    version: str
    url_path: str
    display_name: str


InventoryEntries = t.List[t.Tuple[str, InventoryItem]]


class InventoryManager:
    def __init__(self, location: str):
        self.location = location

    def soi_factory(self) -> soi.Inventory:
        resource_type = ResourceType.detect(self.location)
        if resource_type is ResourceType.PATH:
            return soi.Inventory(source=self.location)
        elif resource_type is ResourceType.URL:
            return soi.Inventory(url=self.location)
        else:  # pragma: nocover
            raise TypeError(f"Unknown inventory type: {self.location}")


class InventoryFormatter:
    """
    Decode and process intersphinx inventories created by Sphinx.

    https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
    """

    def __init__(self, url: str, labels_only: bool = False, omit_documents: bool = False):
        self.url = url
        self.labels_only = labels_only
        self.omit_documents = omit_documents

        self.invman = InventoryManager(location=self.url)
        self.soi = self.invman.soi_factory()
        self.name = self.soi.project

    def to_text_inspect(self):
        inspect_main([self.url])

    def to_text_plain(self):
        print(self.soi.data_file().decode("utf-8"))

    def to_restructuredtext(self):
        line = len(self.name) * "#"
        print(line)
        print(self.name)
        print(line)
        print("\n".join(sorted(self.soi.objects_rst)))

    # ruff: noqa: T201 `print` found
    def to_markdown(self, format_: str = ""):
        class MockConfig:
            intersphinx_timeout: t.Union[int, None] = None
            tls_verify = False
            tls_cacerts: t.Union[str, t.Dict[str, str], None] = None
            user_agent: str = ""

        class MockApp:
            srcdir = ""
            config = MockConfig()

        app = t.cast(Sphinx, MockApp())
        inv_data = fetch_inventory(app, "", self.url)
        print(f"# {self.name}")
        print()
        for key in sorted(inv_data or {}):
            if self.labels_only and key != "std:label":
                continue
            if self.omit_documents and key == "std:doc":
                continue
            print(f"## {key}")
            inv_entries = sorted(inv_data[key].items())
            if format_.endswith("+table"):
                print(tabulate.tabulate(inv_entries, headers=("Reference", "Inventory Record (raw)"), tablefmt="pipe"))
            else:
                print("```text")
                records = self.decode_entries(key, inv_entries)
                for line in self.format_records(records):
                    print(line)
                print("```")
            print()

    def to_html(self, format_: str = ""):
        """
        Format intersphinx repository using HTML.

        TODO: Reference implementation by @webknjaz.
        https://webknjaz.github.io/intersphinx-untangled/setuptools.rtfd.io/
        """
        print(f"""<a id="{self.name}"></a>""")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.to_markdown(format_)
        buffer.seek(0)
        markdown = buffer.read()
        html = markdown_to_html(markdown)
        print(html)

    def to_json(self):
        print(self.soi.json_dict())

    def to_yaml(self):
        logger.warning("There is certainly a better way to present an inventory in YAML format")
        print(yaml.dump(self.soi.json_dict()))

    def decode_entries(
        self,
        reference_type: str,
        inv_entries: InventoryEntries,
    ) -> t.Generator[InventoryRecord, None, None]:
        """
        Decode inv_entries, as per `fetch_inventory`.
        item: (_proj, _ver, url_path, display_name)
        """
        for name, entry in inv_entries:
            yield InventoryRecord(reference_type, name, *entry)

    def format_records(self, records: t.Iterable[InventoryRecord]) -> t.Generator[str, None, None]:
        yield (f"{'Reference': <40} {'Display Name': <40} {'Path'}")
        yield (f"{'---------': <40} {'------------': <40} {'----'}")
        for record in records:
            display_name_effective = record.display_name * (record.display_name != "-")
            yield (f"{record.name: <40} {display_name_effective: <40} {record.url_path}")
