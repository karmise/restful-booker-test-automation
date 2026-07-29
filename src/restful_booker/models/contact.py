"""Contact form models."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ContactMessage:
    """Data entered into the public contact form."""

    name: str
    email: str
    phone: str
    subject: str
    message: str
