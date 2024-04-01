from enum import Enum


class AutoStrEnum(str, Enum):
    """
    StrEnum where enum.auto() returns the field name.
    See https://docs.python.org/3.9/library/enum.html#using-automatic-values

    From https://stackoverflow.com/a/74539097.
    """

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> str:  # noqa: ARG004
        return name


class AutoStrEnumLCase(str, Enum):  # pragma: nocover
    """
    From https://stackoverflow.com/a/74539097.
    """

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):  # noqa: ARG004
        return name.lower()
