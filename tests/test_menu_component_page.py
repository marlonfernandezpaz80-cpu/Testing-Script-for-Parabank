from playwright.sync_api import Page
from pages.update_profile_page import UpdateProfilePage
from pages.accounts_overview_page import AccountsOverviewPage
from pages.bill_pay_page import BillPayPage
from pages.find_transactions_page import FindTransactionsPage
from pages.open_new_account_page import OpenNewAccountPage
from pages.login_page import LoginPage
from pages.transfer_funds_page import TransferFundsPage


def test_open_accounts_overview_page(page: Page, logged_user):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()

def test_open_update_profile_page(page: Page, logged_user):
    logged_user.update_contact_info()
    update_profile_page = UpdateProfilePage(page)
    update_profile_page.is_loaded()

def test_open_find_transactions_page(page: Page, logged_user):
    logged_user.find_transactions()
    find_transactions_page = FindTransactionsPage(page)
    find_transactions_page.is_loaded()

def test_open_bill_pay_page(page: Page, logged_user):
    logged_user.bill_pay()
    bill_pay_page = BillPayPage(page)
    bill_pay_page.is_loaded()

def test_open_open_new_account_page(page: Page, logged_user):
    logged_user.open_new_account()
    open_new_account_page = OpenNewAccountPage(page)
    open_new_account_page.is_loaded()

def test_open_transfer_funds_page(page: Page, logged_user):
    logged_user.transfer_funds()
    transfer_funds_page =TransferFundsPage(page)
    transfer_funds_page.is_loaded()

def test_log_out(page: Page, logged_user):
    logged_user.log_out()
    login_page = LoginPage(page)
    login_page.is_loaded()