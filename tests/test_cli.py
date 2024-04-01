import pytest

from linksmith.cli import cli
from tests.config import OBJECTS_INV_PATH, OBJECTS_INV_URL


def test_cli_version(cli_runner):
    """
    CLI test: Invoke `linksmith --version`.
    """
    result = cli_runner.invoke(
        cli,
        args="--version",
        catch_exceptions=False,
    )
    assert result.exit_code == 0


def test_cli_output_formats(cli_runner):
    """
    CLI test: Invoke `linksmith output-formats`.
    """
    result = cli_runner.invoke(
        cli,
        args="output-formats",
        catch_exceptions=False,
    )
    assert result.exit_code == 0


def test_cli_inventory_no_input(cli_runner):
    """
    CLI test: Invoke `linksmith inventory`.
    """
    result = cli_runner.invoke(
        cli,
        args="inventory",
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert "No input" in result.output


def test_cli_inventory_unknown_input(cli_runner):
    """
    CLI test: Invoke `linksmith inventory example.foo`.
    """
    result = cli_runner.invoke(
        cli,
        args="inventory example.foo",
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert "Unknown input file type: example.foo" in result.output


def test_cli_inventory_unknown_input_with_debug(cli_runner):
    """
    CLI test: Invoke `linksmith inventory example.foo`.
    """
    with pytest.raises(NotImplementedError) as ex:
        cli_runner.invoke(
            cli,
            args="--debug inventory example.foo",
            catch_exceptions=False,
        )
    assert ex.match("Unknown input file type: example.foo")


def test_cli_single_inventory_path(cli_runner):
    """
    CLI test: Invoke `linksmith inventory tests/assets/linksmith.inv --format=text`.
    """
    result = cli_runner.invoke(
        cli,
        args=f"inventory {OBJECTS_INV_PATH} --format=text",
        catch_exceptions=False,
    )
    assert result.exit_code == 0


def test_cli_single_inventory_url(cli_runner):
    """
    CLI test: Invoke `linksmith inventory https://linksmith.readthedocs.io/en/latest/objects.inv --format=text`.
    """
    result = cli_runner.invoke(
        cli,
        args=f"inventory {OBJECTS_INV_URL} --format=text",
        catch_exceptions=False,
    )
    assert result.exit_code == 0


def test_cli_multiple_inventories_path(cli_runner):
    """
    CLI test: Invoke `linksmith inventory tests/assets/index.txt --format=text`.
    """
    result = cli_runner.invoke(
        cli,
        args="inventory tests/assets/index.txt --format=text",
        catch_exceptions=False,
    )
    assert result.exit_code == 0
