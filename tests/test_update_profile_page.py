from playwright.sync_api import Page, expect
from pages.update_profile_page import UpdateProfilePage
from pages.utils import generate_user
import pytest

@pytest.mark.parametrize("with_plus", [
    False,
    pytest.param(True, marks=pytest.mark.xfail(
        reason='Parabank convierte el "+" del telefono en un espacio', strict=True, raises=AssertionError))

], ids=["phone_without_plus", "phone_with_plus"])
def test_update_profile(page: Page, logged_user, with_plus):
    logged_user.update_contact_info()
    update_profile_page = UpdateProfilePage(page)
    update_profile_page.is_loaded()
    user = generate_user(with_plus)
    update_profile_page.fill_first_name(user["first_name"])
    update_profile_page.fill_last_name(user["last_name"])
    update_profile_page.fill_address(user["address"])
    update_profile_page.fill_city(user["city"])
    update_profile_page.fill_state(user["state"])
    update_profile_page.fill_zip_code(user["zip_code"])
    update_profile_page.fill_phone_number(user["phone_number"])
    update_profile_page.click_update_profile_button()
    update_profile_page.profile_was_updated()
    page.reload()
    update_profile_page.is_loaded()
    expect(update_profile_page.first_name_textbox).to_have_value(user["first_name"])
    expect(update_profile_page.last_name_textbox).to_have_value(user["last_name"])
    expect(update_profile_page.address_textbox).to_have_value(user["address"])
    expect(update_profile_page.city_textbox).to_have_value(user["city"])
    expect(update_profile_page.state_textbox).to_have_value(user["state"])
    expect(update_profile_page.zip_code_textbox).to_have_value(user["zip_code"])
    expect(update_profile_page.phone_number_textbox).to_have_value(user["phone_number"])

