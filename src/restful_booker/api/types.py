"""Shared JSON-compatible value types for API serialization."""

from typing import TypeAlias

JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
QueryValue: TypeAlias = str | int | float | None
