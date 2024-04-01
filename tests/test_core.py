import io

import pytest

from linksmith.model import OutputFormatRegistry
from linksmith.sphinx.core import inventories_to_text, inventory_to_text
from tests.config import OBJECTS_INV_PATH, OBJECTS_INV_URL


@pytest.mark.parametrize("format_", OutputFormatRegistry.aliases())
def test_single_inventory_path(format_: str):
    inventory_to_text(OBJECTS_INV_PATH, format_)


@pytest.mark.parametrize("format_", OutputFormatRegistry.aliases())
def test_single_inventory_url(format_: str):
    inventory_to_text(OBJECTS_INV_URL, format_)


@pytest.mark.parametrize("format_", OutputFormatRegistry.aliases())
def test_multiple_inventories_path(format_: str):
    inventories_to_text("tests/assets/index.txt", format_)


@pytest.mark.parametrize("format_", OutputFormatRegistry.aliases())
def test_multiple_inventories_buffer(format_: str):
    urls = io.StringIO(
        """
tests/assets/linksmith.inv
tests/assets/sde.inv
    """.strip(),
    )
    inventories_to_text(urls, format_)


@pytest.mark.skip("Does not work yet")
def test_multiple_inventories_url():
    url = "https://github.com/tech-writing/linksmith/raw/main/tests/assets/index.txt"
    inventories_to_text(url, "html")


def test_unknown_output_format():
    with pytest.raises(NotImplementedError) as ex:
        inventory_to_text(OBJECTS_INV_PATH, "foo-format")
    ex.match("Output format not implemented: foo-format")


def test_unknown_input_format_single():
    with pytest.raises(NotImplementedError) as ex:
        inventory_to_text("foo.bar", "text")
    ex.match("Resource type not implemented: foo.bar")


def test_unknown_input_format_multiple():
    with pytest.raises(NotImplementedError) as ex:
        inventories_to_text("foo.bar", "text")
    ex.match("Resource type not implemented: foo.bar")
