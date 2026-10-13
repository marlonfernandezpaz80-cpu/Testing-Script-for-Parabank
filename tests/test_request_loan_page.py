from playwright.sync_api import Page
from pages.request_loan_page import RequestLoanPage
from pages.accounts_overview_page import AccountsOverviewPage
from pages.account_activity_page import AccountsActivityPage
import pytest

@pytest.mark.creates_data
def test_request_loan(page: Page, logged_user):
    logged_user.request_loan()
    request_loan_page = RequestLoanPage(page)
    request_loan_page.is_loaded()
    selected_account = request_loan_page.get_an_account()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.open()
    accounts_overview_page.is_loaded()
    print(selected_account)
    account_initial_balance = accounts_overview_page.get_account_balance(selected_account)
    request_loan_page.open()
    loan_amount = "10"
    down_payment = "8"
    request_loan_page.fill_amount(loan_amount)
    request_loan_page.fill_down_payment(down_payment)
    request_loan_page.select_account(selected_account)
    request_loan_page.click_apply_now()
    request_loan_page.loan_processed()
    request_loan_page.loan_is_approved()
    new_account = request_loan_page.get_new_account_id()
    accounts_overview_page.open()
    accounts_overview_page.is_loaded()
    account_final_balance = accounts_overview_page.get_account_balance(selected_account)
    assert float(account_final_balance) == float(account_initial_balance) - float(down_payment)
    new_account_balance = accounts_overview_page.get_account_balance(new_account)
    assert float(new_account_balance) == float(loan_amount)
    accounts_overview_page.click_account(new_account)
    accounts_activity_page = AccountsActivityPage(page)
    accounts_activity_page.is_loaded()
    accounts_activity_page.confirm_account(new_account)
    new_account_type = accounts_activity_page.get_account_type()
    assert new_account_type == "LOAN"