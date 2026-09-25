"""Expected success fields in mutation responses; extra fields remain permitted."""

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

SUCCESS_RESPONSE: Final[Mapping[str, bool]] = MappingProxyType({"success": True})
