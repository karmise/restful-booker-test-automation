"""Contact labels, validation fragments and successful submission template."""

from typing import Final

HEADING: Final = "Send Us a Message"
SUBMIT: Final = "Submit"
REQUIRED_FIELD_ERRORS: Final = (
    "Name may not be blank",
    "Email may not be blank",
    "Phone may not be blank",
    "Subject may not be blank",
    "Message may not be blank",
)
INVALID_EMAIL: Final = "must be a well-formed email address"
INVALID_PHONE: Final = "Phone must be between 11 and 21 characters."
SUBMISSION_CONFIRMATION: Final = "Thanks for getting in touch {name}!"
