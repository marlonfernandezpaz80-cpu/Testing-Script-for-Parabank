from playwright.sync_api import Page, expect
import pytest
from pages.accounts_overview_page import AccountsOverviewPage
from pages.open_new_account_page import OpenNewAccountPage

@pytest.mark.creates_data
@pytest.mark.parametrize("account_type", ["0", "1"])
def test_account_creation(account_type, logged_user, page: Page):
    logged_user.open_new_account()
    open_new_account_page = OpenNewAccountPage(page)
    open_new_account_page.is_loaded()
    open_new_account_page.select_account_type(account_type)
    option = open_new_account_page.get_random_account_options()
    open_new_account_page.select_account(option)
    open_new_account_page.click_open_account()
    open_new_account_page.account_opened()
    account_number = open_new_account_page.get_new_account_number()
    accounts_overview = AccountsOverviewPage(page)
    accounts_overview.open()
    accounts_list = accounts_overview.get_accounts_list()
    assert account_number in accounts_list
