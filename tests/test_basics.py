import sphobjinv as soi

from linksmith import dummy


def test_dummy():
    assert dummy() == 42


def test_sphobjinv():
    objects_inv = "https://sphobjinv.readthedocs.io/en/stable/objects.inv"
    inv = soi.Inventory(url=objects_inv)
    assert inv.project == "sphobjinv"
    assert inv.version == "2.3"
    assert inv.source_type is soi.SourceTypes.URL
