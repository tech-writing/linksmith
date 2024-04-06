import dataclasses
import io
import typing as t
from enum import auto
from pathlib import Path

from linksmith.util.python import AutoStrEnum


class OutputFormat(AutoStrEnum):
    TEXT_INSPECT = auto()
    TEXT_PLAIN = auto()
    MARKDOWN = auto()
    MARKDOWN_TABLE = auto()
    RESTRUCTUREDTEXT = auto()
    HTML = auto()
    HTML_TABLE = auto()
    JSON = auto()
    YAML = auto()


@dataclasses.dataclass
class OutputFormatRule:
    format: OutputFormat
    aliases: t.List[str]


class OutputFormatRegistry:
    rules = [
        OutputFormatRule(format=OutputFormat.TEXT_INSPECT, aliases=["text"]),
        OutputFormatRule(format=OutputFormat.TEXT_PLAIN, aliases=["text+plain"]),
        OutputFormatRule(format=OutputFormat.MARKDOWN, aliases=["markdown", "md"]),
        OutputFormatRule(format=OutputFormat.MARKDOWN_TABLE, aliases=["markdown+table", "md+table"]),
        OutputFormatRule(format=OutputFormat.RESTRUCTUREDTEXT, aliases=["restructuredtext", "rst"]),
        OutputFormatRule(format=OutputFormat.HTML, aliases=["html", "html+table"]),
        OutputFormatRule(format=OutputFormat.JSON, aliases=["json"]),
        OutputFormatRule(format=OutputFormat.YAML, aliases=["yaml"]),
    ]

    @classmethod
    def resolve(cls, format_: str) -> OutputFormat:
        for rule in cls.rules:
            if format_ in rule.aliases:
                return rule.format
        raise NotImplementedError(f"Output format not implemented: {format_}")

    @classmethod
    def aliases(cls) -> t.List[str]:
        data = []
        for rule in cls.rules:
            data += rule.aliases
        return data


class ResourceType(AutoStrEnum):
    LIST = auto()
    BUFFER = auto()
    PATH = auto()
    URL = auto()

    @classmethod
    def detect(cls, location):
        if isinstance(location, list):
            return cls.LIST
        if isinstance(location, io.IOBase):
            return cls.BUFFER
        if location.startswith("http://") or location.startswith("https://"):
            return cls.URL
        path = Path(location)
        if path.exists():
            return cls.PATH
        else:
            raise FileNotFoundError(f"Resource not found: {location}")
