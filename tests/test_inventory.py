from unittest.mock import patch

import pytest

from linksmith.sphinx.core import dump_inventory_universal
from linksmith.sphinx.inventory import InventoryFormatter, InventoryManager
from tests.config import OBJECTS_INV_PATH


def test_inventory_labels_only(capsys):
    inventory = InventoryFormatter(url=OBJECTS_INV_PATH, labels_only=True)
    inventory.to_markdown()
    out, err = capsys.readouterr()
    assert "std:label" in out
    assert "std:doc" not in out


def test_inventory_omit_documents(capsys):
    inventory = InventoryFormatter(url=OBJECTS_INV_PATH, omit_documents=True)
    inventory.to_markdown()
    out, err = capsys.readouterr()
    assert "std:label" in out
    assert "std:doc" not in out


def test_inventory_manager_file_not_found():
    invman = InventoryManager("foo")
    with pytest.raises(FileNotFoundError) as ex:
        invman.soi_factory()
    assert ex.match("Resource not found: foo")


def test_cli_inventory_autodiscover(capsys):
    """
    Verify local `objects.inv` auto-discovery works.
    """
    with patch("linksmith.sphinx.util.LocalObjectsInv.objects_inv_candidates", ["tests/assets/linksmith.inv"]):
        dump_inventory_universal([])
    out, err = capsys.readouterr()
    assert "std:doc" in out
    assert "std:label" in out


def test_inventory_no_input():
    """
    Exercise a failing auto-discovery, where absolutely no input files can be determined.
    """
    with patch("linksmith.sphinx.util.LocalObjectsInv.objects_inv_candidates", []):
        with pytest.raises(FileNotFoundError) as ex:
            dump_inventory_universal([])
        ex.match("No inventory specified, and none discovered: No objects.inv found in working directory")
