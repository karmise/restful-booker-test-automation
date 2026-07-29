"""JSON Schema loading and readable contract validation."""

from __future__ import annotations

import json
from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path
from typing import cast

from jsonschema import FormatChecker
from jsonschema.validators import validator_for

from restful_booker.api.types import JsonValue


class SchemaRegistry:
    """Load named schemas and report every response-contract violation."""

    def __init__(self, schema_directory: Path | None = None) -> None:
        self._schema_directory = schema_directory or Path(__file__).with_name("schemas")

    def validate(self, instance: JsonValue, schema_name: str) -> None:
        """Validate a JSON-compatible value against a named schema."""

        schema = self._load_schema(self._schema_directory, schema_name)
        validator_class = validator_for(schema)
        validator_class.check_schema(schema)
        validator = validator_class(schema, format_checker=FormatChecker())
        errors = sorted(
            validator.iter_errors(instance),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
        if not errors:
            return

        details = "\n".join(
            f"- {_json_path(error.absolute_path)}: {error.message}" for error in errors
        )
        raise AssertionError(f"Response does not match JSON Schema '{schema_name}':\n{details}")

    @staticmethod
    @lru_cache
    def _load_schema(schema_directory: Path, schema_name: str) -> dict[str, object]:
        schema_path = schema_directory / f"{schema_name}.json"
        if not schema_path.is_file():
            raise FileNotFoundError(f"JSON Schema not found: {schema_path}")

        with schema_path.open(encoding="utf-8") as schema_file:
            loaded = json.load(schema_file)
        if not isinstance(loaded, dict):
            raise TypeError(f"JSON Schema must be an object: {schema_path}")
        return cast(dict[str, object], loaded)


def _json_path(parts: Iterable[object]) -> str:
    rendered = "$"
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered
