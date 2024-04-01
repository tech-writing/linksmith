import pytest

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


def test_inventory_manager_unknown():
    invman = InventoryManager("foo")
    with pytest.raises(NotImplementedError) as ex:
        invman.soi_factory()
    assert ex.match("Resource type not implemented: foo")
