from playwright.sync_api import Page, expect
import pytest
from pages.login_page import LoginPage
from pages.menu_component import MenuComponent


@pytest.fixture(scope="function")
def logged_user(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username("test_user")
    login_page.fill_password("test_user123")
    login_page.click_login()
    menu_component = MenuComponent(page)
    menu_component.is_loaded()
    #expect(menu_component.error_sign).not_to_be_visible()
    yield menu_component