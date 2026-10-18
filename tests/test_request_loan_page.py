from playwright.sync_api import Page, expect
from pages.request_loan_page import RequestLoanPage
from pages.accounts_overview_page import AccountsOverviewPage
from pages.account_activity_page import AccountsActivityPage
import pytest

#@pytest.mark.creates_data
def test_request_loan(page: Page, logged_user):
    loan_amount = "10"
    down_payment = "8"
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    account = accounts_overview_page.get_random_account()
    account_initial_balance = accounts_overview_page.get_account_balance(account)
    request_loan_page = RequestLoanPage(page)
    request_loan_page.open()
    request_loan_page.is_loaded()
    request_loan_page.fill_amount(loan_amount)
    request_loan_page.fill_down_payment(down_payment)
    request_loan_page.select_account(account)
    request_loan_page.click_apply_now()
    request_loan_page.loan_processed()
    request_loan_page.loan_is_approved()
    new_account = request_loan_page.get_new_account_id()
    accounts_overview_page.open()
    accounts_overview_page.is_loaded()
    account_final_balance = accounts_overview_page.get_account_balance(account)
    assert account_final_balance == account_initial_balance - float(down_payment)
    new_account_balance = accounts_overview_page.get_account_balance(new_account)
    assert new_account_balance == float(loan_amount)
    accounts_overview_page.click_account(new_account)
    accounts_activity_page = AccountsActivityPage(page)
    accounts_activity_page.is_loaded()
    accounts_activity_page.confirm_account(new_account)
    new_account_type = accounts_activity_page.get_account_type()
    assert new_account_type == "LOAN"


@pytest.mark.negative
@pytest.mark.parametrize("loan_amount, down_payment", [
    ("1", "2"),
    ("100000000000", "10"),
    ("", "")
])
def test_request_invalid_loan(page: Page, logged_user, loan_amount, down_payment):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    account = accounts_overview_page.get_random_account()
    account_initial_balance = accounts_overview_page.get_account_balance(account)
    request_loan_page = RequestLoanPage(page)
    request_loan_page.open()
    request_loan_page.is_loaded()
    request_loan_page.fill_amount(loan_amount)
    request_loan_page.fill_down_payment(down_payment)
    request_loan_page.select_account(account)
    request_loan_page.click_apply_now()
    page.wait_for_load_state("networkidle")
    expect(request_loan_page.loan_status).to_contain_text("Denied")
    accounts_overview_page.open()
    accounts_overview_page.is_loaded()
    account_final_balance = accounts_overview_page.get_account_balance(account)
    assert account_final_balance == account_initial_balance