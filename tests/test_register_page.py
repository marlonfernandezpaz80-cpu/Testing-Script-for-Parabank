from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.utils import generate_user
from pages.menu_component import MenuComponent
from playwright.sync_api import Page
import pytest

required_fields = ["first_name", "last_name", "address", "city", "state", "zip_code", "ssn", "username", "password", "confirm_password"]

@pytest.mark.parametrize("missing_field", required_fields)
def test_incomplete_register(page: Page, missing_field):
    login_page = LoginPage(page)
    login_page.open()
    login_page.click_register()
    register_page = RegisterPage(page)
    register_page.is_loaded()
    user = generate_user()
    if missing_field != "confirm_password":
        user[missing_field] = ""
        register_page.fill_confirm_password(user["password"])
    register_page.fill_first_name(user["first_name"])
    register_page.fill_last_name(user["last_name"])
    register_page.fill_address(user["address"])
    register_page.fill_city(user["city"])
    register_page.fill_state(user["state"])
    register_page.fill_zip_code(user["zip_code"])
    register_page.fill_phone_number(user["phone_number"])
    register_page.fill_ssn(user["ssn"])
    register_page.fill_username(user["username"])
    register_page.fill_password(user["password"])
    register_page.click_register()
    register_page.user_not_registered()

def test_register(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.click_register()
    register_page = RegisterPage(page)
    register_page.is_loaded()
    user = generate_user()
    register_page.fill_first_name(user["first_name"])
    register_page.fill_last_name(user["last_name"])
    register_page.fill_address(user["address"])
    register_page.fill_city(user["city"])
    register_page.fill_state(user["state"])
    register_page.fill_zip_code(user["zip_code"])
    register_page.fill_phone_number(user["phone_number"])
    register_page.fill_ssn(user["ssn"])
    register_page.fill_username(user["username"])
    register_page.fill_password(user["password"])
    register_page.fill_confirm_password(user["password"])
    register_page.click_register()
    register_page.user_registered()
    menu_component = MenuComponent(page)
    menu_component.log_out()
    login_page = LoginPage(page)
    login_page.fill_username(user["username"])
    login_page.fill_password(user["password"])
    login_page.click_login()
    menu_component = MenuComponent(page)
    menu_component.is_loaded()
    
    
