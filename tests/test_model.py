import io

import pytest

from linksmith.model import OutputFormat, OutputFormatRegistry, ResourceType


def test_output_format_success():
    assert OutputFormatRegistry.resolve("text") is OutputFormat.TEXT_INSPECT


def test_output_format_unknown():
    with pytest.raises(NotImplementedError) as ex:
        OutputFormatRegistry.resolve("foo-format")
    assert ex.match("Output format not implemented: foo-format")


def test_resource_type_path():
    assert ResourceType.detect("README.md") is ResourceType.PATH


def test_resource_type_url():
    assert ResourceType.detect("http://example.org") is ResourceType.URL


def test_resource_type_buffer():
    buffer = io.StringIO("http://example.org")
    assert ResourceType.detect(buffer) is ResourceType.BUFFER


def test_resource_not_found_file():
    with pytest.raises(FileNotFoundError) as ex:
        ResourceType.detect("foobar")
    assert ex.match("Resource not found: foobar")
