from pages.login_page import LoginPage
from pages.accounts_overview_page import AccountsOverviewPage
from playwright.sync_api import Page, expect
from pages.menu_component import MenuComponent
import pytest
from faker import Faker

fake = Faker()

@pytest.mark.smoke
def test_login(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.fill_username("test_user")
    login_page.fill_password("test_user123")
    login_page.click_login()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    menu_component = MenuComponent(page)
    menu_component.is_loaded()
    expect(menu_component.error_sign).not_to_be_visible()

@pytest.mark.negative
@pytest.mark.parametrize("user", [
    (fake.user_name(), fake.password()),
    ("test_user", fake.password()),
    (fake.user_name(), ""),
    ("", fake.password()),
])
def test_login_fallido(page: Page, user):
    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.fill_username(user[0])
    login_page.fill_password(user[1])
    login_page.click_login()
    expect(login_page.error_sign).to_be_visible()
    if user[0] == "" or user[1] == '':
        expect(login_page.page.get_by_text("Please enter a username and password").first).to_be_visible() 
    else:
        expect(login_page.page.get_by_text("The username and password could not be verified").first).to_be_visible()
    menu_component = MenuComponent(page)
    expect(menu_component.title).not_to_be_visible()