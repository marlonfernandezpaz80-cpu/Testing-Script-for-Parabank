from pages.login_page import LoginPage
from pages.accounts_overview_page import AccountsOverviewPage
from playwright.sync_api import Page, expect
from pages.menu_component import MenuComponent
import pytest

def test_login(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.fill_username("test_user")
    login_page.fill_password("test_user123")
    login_page.click_login()
    accounts_page = AccountsOverviewPage(page)
    accounts_page.is_loaded()
    menu_component = MenuComponent(page)
    menu_component.is_loaded()
    expect(menu_component.error_sign).not_to_be_visible()
