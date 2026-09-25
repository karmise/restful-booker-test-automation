"""Authentication response contract; error strings are matched as substrings."""

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

INVALID_CREDENTIALS: Final = "Invalid credentials"
INVALID_TOKEN: Final = "Invalid token"
AUTHENTICATION_REQUIRED: Final = "Authentication required"
MIN_TOKEN_LENGTH: Final = 16
VALID_TOKEN_RESPONSE: Final[Mapping[str, bool]] = MappingProxyType({"valid": True})
