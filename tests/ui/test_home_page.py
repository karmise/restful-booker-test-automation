"""Home page UI scenarios."""

import pytest
from playwright.sync_api import expect

from restful_booker.models import ContactMessage
from restful_booker.ui.pages import HomePage, ReservationPage


@pytest.mark.ui
@pytest.mark.smoke
def test_user_opens_a_seeded_room(
    home_page: HomePage,
    reservation_page: ReservationPage,
) -> None:
    home_page.open()

    expect(home_page.room_card("Double")).to_be_visible()
    home_page.open_room("Double")

    reservation_page.expect_open_for(room_id=2, room_name="Double")


@pytest.mark.ui
@pytest.mark.regression
def test_contact_form_reports_required_fields(home_page: HomePage) -> None:
    home_page.open()

    home_page.contact_form.submit_empty()

    expect(home_page.contact_form.validation_feedback).to_contain_text("Name may not be blank")
    expect(home_page.contact_form.validation_feedback).to_contain_text("Email may not be blank")
    expect(home_page.contact_form.validation_feedback).to_contain_text("Phone may not be blank")
    expect(home_page.contact_form.validation_feedback).to_contain_text("Subject may not be blank")
    expect(home_page.contact_form.validation_feedback).to_contain_text("Message may not be blank")


@pytest.mark.ui
@pytest.mark.smoke
def test_user_submits_a_valid_contact_message(
    home_page: HomePage,
    contact_message: ContactMessage,
) -> None:
    home_page.open()

    home_page.contact_form.submit(contact_message)

    expect(
        home_page.contact_form.confirmation(f"Thanks for getting in touch {contact_message.name}!")
    ).to_be_visible()
    expect(home_page.contact_form.confirmation(contact_message.subject)).to_be_visible()
