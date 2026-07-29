"""Strict helpers for parsing JSON values into response DTOs."""

from collections.abc import Mapping
from typing import cast


def as_object(value: object, *, context: str) -> Mapping[str, object]:
    """Require a JSON object."""

    if not isinstance(value, dict):
        raise TypeError(f"{context} must be a JSON object, got {type(value).__name__}")
    return cast(dict[str, object], value)


def as_array(value: object, *, context: str) -> list[object]:
    """Require a JSON array."""

    if not isinstance(value, list):
        raise TypeError(f"{context} must be a JSON array, got {type(value).__name__}")
    return cast(list[object], value)


def required_str(data: Mapping[str, object], key: str) -> str:
    """Read a required string field."""

    value = data.get(key)
    if not isinstance(value, str):
        raise TypeError(f"'{key}' must be a string")
    return value


def required_int(data: Mapping[str, object], key: str) -> int:
    """Read a required integer field without accepting booleans."""

    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"'{key}' must be an integer")
    return value


def required_bool(data: Mapping[str, object], key: str) -> bool:
    """Read a required boolean field."""

    value = data.get(key)
    if not isinstance(value, bool):
        raise TypeError(f"'{key}' must be a boolean")
    return value


def required_str_tuple(data: Mapping[str, object], key: str) -> tuple[str, ...]:
    """Read a required array of strings."""

    values = as_array(data.get(key), context=f"'{key}'")
    if not all(isinstance(value, str) for value in values):
        raise TypeError(f"'{key}' must contain only strings")
    return tuple(cast(list[str], values))
