"""Expected availability report content."""

from typing import Final

UNAVAILABLE_TITLE: Final = "Unavailable"


def empty_room_report() -> dict[str, list[object]]:
    """Return a fresh expected envelope so mutable lists are never shared."""

    return {"report": []}
