from playwright.sync_api import Page, expect
import random
from pages.accounts_overview_page import AccountsOverviewPage
from pages.transfer_funds_page import TransferFundsPage
import pytest

def test_transfer_funds(page: Page, logged_user):
    amount = 2
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    accounts_list = accounts_overview_page.get_accounts_list()
    if len(accounts_list) > 1:
        from_account = accounts_overview_page.get_random_account()
        from_account_initial_balance = accounts_overview_page.get_account_balance(from_account)
        to_account = ""
        while True:
            account = accounts_overview_page.get_random_account()
            if account != from_account:
                to_account = account
                break           
        to_account_initial_balance = accounts_overview_page.get_account_balance(to_account)
        transfer_funds_page = TransferFundsPage(page)
        transfer_funds_page.open()
        transfer_funds_page.is_loaded()
        transfer_funds_page.set_amount(amount)
        transfer_funds_page.source_account(from_account)
        transfer_funds_page.destination_account(to_account)
        transfer_funds_page.click_transfer()
        transfer_funds_page.transfer_is_complete()
        transfer_funds_page.from_account_is_right(from_account)
        transfer_funds_page.to_account_is_right(to_account)
        accounts_overview_page.open()
        accounts_overview_page.is_loaded()
        from_account_final_balance = accounts_overview_page.get_account_balance(from_account)
        assert from_account_final_balance == from_account_initial_balance - amount
        to_account_final_balance = accounts_overview_page.get_account_balance(to_account)
        assert to_account_final_balance == to_account_initial_balance + amount

@pytest.mark.negative
@pytest.mark.parametrize("amount", [0, -2, "", "dos"])
def test_transfer_invalid_funds(page: Page, logged_user, amount):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    accounts_list = accounts_overview_page.get_accounts_list()
    if len(accounts_list) > 1:
        from_account = accounts_overview_page.get_random_account()
        from_account_initial_balance = accounts_overview_page.get_account_balance(from_account)
        to_account = ""
        while True:
            account = accounts_overview_page.get_random_account()
            if account != from_account:
                to_account = account
                break           
        to_account_initial_balance = accounts_overview_page.get_account_balance(to_account)
        transfer_funds_page = TransferFundsPage(page)
        transfer_funds_page.open()
        transfer_funds_page.is_loaded()
        transfer_funds_page.set_amount(amount)
        transfer_funds_page.source_account(from_account)
        transfer_funds_page.destination_account(to_account)
        transfer_funds_page.click_transfer()
        page.wait_for_load_state("networkidle")
        expect(transfer_funds_page.transfer_complete_sign).not_to_be_visible()
        accounts_overview_page.open()
        accounts_overview_page.is_loaded()
        from_account_final_balance = accounts_overview_page.get_account_balance(from_account)
        assert from_account_final_balance == from_account_initial_balance
        to_account_final_balance = accounts_overview_page.get_account_balance(to_account)
        assert to_account_final_balance == to_account_initial_balance
