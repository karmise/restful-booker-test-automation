"""Reservation labels, validation fragments and pricing presentation."""

from typing import Final

RESERVE: Final = "Reserve Now"
CANCEL: Final = "Cancel"
FIRST_NAME_LABEL: Final = "Firstname"
LAST_NAME_LABEL: Final = "Lastname"
EMAIL_LABEL: Final = "Email"
PHONE_LABEL: Final = "Phone"
FIRST_NAME_REQUIRED: Final = "Firstname should not be blank"
LAST_NAME_REQUIRED: Final = "Lastname should not be blank"
INVALID_EMAIL: Final = "must be a well-formed email address"
INVALID_PHONE: Final = "size must be between 11 and 21"
ROOM_HEADING: Final = "{room_type} Room"
ROOM_IMAGE_ALT: Final = "Room Image"
PRICE_LINE: Final = "£{nightly_rate} x {nights} nights"
TOTAL_PRICE: Final = "£{amount}"
SERVICE_FEE_GBP: Final = 40
