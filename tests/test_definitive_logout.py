from pages.accounts_overview_page import AccountsOverviewPage
from pages.account_activity_page import AccountsActivityPage
from pages.open_new_account_page import OpenNewAccountPage
from pages.bill_pay_page import BillPayPage
from pages.find_transactions_page import FindTransactionsPage
from pages.request_loan_page import RequestLoanPage
from pages.transaction_details_page import TransactionDetailsPage
from pages.transfer_funds_page import TransferFundsPage
from pages.update_profile_page import UpdateProfilePage
from pages.menu_component import MenuComponent
from pages.login_page import LoginPage
from playwright.sync_api import Page, expect
from pages.utils import get_account_with_activity
import pytest

main_pages = [AccountsOverviewPage, OpenNewAccountPage, BillPayPage, FindTransactionsPage, RequestLoanPage, TransferFundsPage, UpdateProfilePage]


@pytest.mark.negative
@pytest.mark.parametrize("main_page", main_pages)
def test_protected_page_after_logout(page: Page, logged_user, main_page):
    target_page = main_page(page)
    target_page.open()
    target_page.is_loaded()
    url = page.url
    MenuComponent(page).log_out()
    login_page = LoginPage(page)
    login_page.is_loaded()
    page.goto(url)
    expect(login_page.title).to_be_visible()
    expect(target_page.title).not_to_be_visible()


@pytest.mark.negative    
def test_definitive_logout_from_account_activity_page(page: Page, logged_user):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    account = accounts_overview_page.get_random_account()
    accounts_overview_page.click_account(account)
    account_activity_page = AccountsActivityPage(page)
    account_activity_page.is_loaded()
    url = page.url
    menu_component = MenuComponent(page)
    menu_component.is_loaded()
    menu_component.log_out()
    login_page = LoginPage(page)
    login_page.is_loaded()
    page.goto(url)
    expect(account_activity_page.account_number).not_to_contain_text(account)
    expect(page.get_by_role("heading", name="Error!").first).to_be_visible()
    login_page.is_loaded()


@pytest.mark.negative
@pytest.mark.xfail(raises=AssertionError, strict=True, reason="En local, transaction.htm?id=X devuelve los datos sin sesión (contexto limpio e incógnito)")
def test_definitive_logout_from_transactions_details_page(page: Page, logged_user, browser):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    accounts = accounts_overview_page.get_accounts_list()
    account = get_account_with_activity(accounts, page)
    accounts_overview_page.open()
    accounts_overview_page.is_loaded()
    accounts_overview_page.click_account(account)
    account_activity_page = AccountsActivityPage(page)
    account_activity_page.is_loaded()
    transaction_index = account_activity_page.get_a_line_index() 
    account_activity_page.click_transaction(transaction_index)
    transaction_details_page = TransactionDetailsPage(page)
    transaction_details_page.is_loaded()
    url = page.url
    transaction_id = transaction_details_page.get_transaction_id()
    menu_component = MenuComponent(page)
    menu_component.is_loaded()
    menu_component.log_out()
    context = browser.new_context()
    new_page = context.new_page()
    new_page.goto(url)
    expect(new_page.get_by_text(transaction_id)).not_to_be_visible()
    expect(new_page.get_by_role("heading", name="Error!").first).to_be_visible()
