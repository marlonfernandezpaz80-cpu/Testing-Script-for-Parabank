from playwright.sync_api import expect, Page
from pages.bill_pay_page import BillPayPage
from pages.accounts_overview_page import AccountsOverviewPage
import pytest
from pages.utils import generate_user

@pytest.mark.smoke
def test_bill_pay(logged_user, page: Page):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    account = accounts_overview_page.get_random_account()
    account_initial_balance = accounts_overview_page.get_account_balance(account)
    bill_pay_page = BillPayPage(page)
    bill_pay_page.open()
    bill_pay_page.is_loaded()
    user = generate_user()
    bill_pay_page.fill_payee_name(user["first_name"])
    bill_pay_page.fill_address(user["address"])
    bill_pay_page.fill_city(user["city"])
    bill_pay_page.fill_state(user["state"])
    bill_pay_page.fill_zip_code(user["zip_code"])
    bill_pay_page.fill_phone(user["phone_number"])
    bill_pay_page.fill_account(user["account"])
    bill_pay_page.fill_verify_account(user["account"])
    amount = 1
    bill_pay_page.fill_amount(str(amount))
    bill_pay_page.select_from_account(account)
    bill_pay_page.click_send_payment()
    bill_pay_page.payment_finished()
    accounts_overview_page.open()
    accounts_overview_page.is_loaded()
    account_final_balance = accounts_overview_page.get_account_balance(account)
    assert account_final_balance == account_initial_balance - amount
    
required_information = ["first_name", "address", "city", "state", "zip_code", "phone_number", "account", "account2"]

@pytest.mark.negative
@pytest.mark.parametrize("empty_info", required_information)
def test_bill_pay_with_empty_info(page: Page, logged_user, empty_info):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    account = accounts_overview_page.get_random_account()
    account_initial_balance = accounts_overview_page.get_account_balance(account)
    bill_pay_page = BillPayPage(page)
    bill_pay_page.open()
    bill_pay_page.is_loaded()
    user = generate_user()
    amount = 1
    if empty_info == "account":
        bill_pay_page.fill_payee_name(user["first_name"])
        bill_pay_page.fill_address(user["address"])
        bill_pay_page.fill_city(user["city"])
        bill_pay_page.fill_state(user["state"])
        bill_pay_page.fill_zip_code(user["zip_code"])
        bill_pay_page.fill_phone(user["phone_number"])
        bill_pay_page.fill_account("")
        bill_pay_page.fill_verify_account(user["account"])
        bill_pay_page.fill_amount(str(amount))
        bill_pay_page.select_from_account(account)
        bill_pay_page.click_send_payment()
        bill_pay_page.is_loaded()
        expect(page.get_by_text("The account numbers do not match.").first).to_be_visible()
        bill_pay_page.payment_not_finished()
        accounts_overview_page.open()
    elif empty_info == "account2":
        bill_pay_page.fill_payee_name(user["first_name"])
        bill_pay_page.fill_address(user["address"])
        bill_pay_page.fill_city(user["city"])
        bill_pay_page.fill_state(user["state"])
        bill_pay_page.fill_zip_code(user["zip_code"])
        bill_pay_page.fill_phone(user["phone_number"])
        bill_pay_page.fill_account(user["account"])
        bill_pay_page.fill_verify_account("")
        bill_pay_page.fill_amount(str(amount))
        bill_pay_page.select_from_account(account)
        bill_pay_page.click_send_payment()
        bill_pay_page.is_loaded()
        bill_pay_page.payment_not_finished()   
    else:
        user[empty_info] =""
        bill_pay_page.fill_payee_name(user["first_name"])
        bill_pay_page.fill_address(user["address"])
        bill_pay_page.fill_city(user["city"])
        bill_pay_page.fill_state(user["state"])
        bill_pay_page.fill_zip_code(user["zip_code"])
        bill_pay_page.fill_phone(user["phone_number"])
        bill_pay_page.fill_account(user["account"])
        bill_pay_page.fill_verify_account(user["account"])
        bill_pay_page.fill_amount(str(amount))
        bill_pay_page.select_from_account(account)
        bill_pay_page.click_send_payment()
        bill_pay_page.is_loaded()
        bill_pay_page.payment_not_finished()
    accounts_overview_page.open()
    accounts_overview_page.is_loaded()
    account_final_balance = accounts_overview_page.get_account_balance(account)
    assert account_final_balance == account_initial_balance

@pytest.mark.negative
@pytest.mark.parametrize("amount", [
    pytest.param(0, marks=pytest.mark.xfail(raises=AssertionError, strict=True, reason="Se permite pagar factura con $0")),
    pytest.param(-2, marks=pytest.mark.xfail(raises=AssertionError, strict=True, reason="Se permite pagar factura con un monto negativo")),
    "",
    "dos"

])
def test_bill_pay_with_invalid_amount(page: Page, logged_user, amount):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    account = accounts_overview_page.get_random_account()
    account_initial_balance = accounts_overview_page.get_account_balance(account)
    bill_pay_page = BillPayPage(page)
    bill_pay_page.open()
    bill_pay_page.is_loaded()
    user = generate_user()
    bill_pay_page.fill_payee_name(user["first_name"])
    bill_pay_page.fill_address(user["address"])
    bill_pay_page.fill_city(user["city"])
    bill_pay_page.fill_state(user["state"])
    bill_pay_page.fill_zip_code(user["zip_code"])
    bill_pay_page.fill_phone(user["phone_number"])
    bill_pay_page.fill_account(user["account"])
    bill_pay_page.fill_verify_account(user["account"])
    bill_pay_page.fill_amount(str(amount))
    bill_pay_page.select_from_account(account)
    bill_pay_page.click_send_payment()
    page.wait_for_load_state("networkidle")
    bill_pay_page.payment_not_finished()
    accounts_overview_page.open()
    accounts_overview_page.is_loaded()
    account_final_balance = accounts_overview_page.get_account_balance(account)
    assert account_final_balance == account_initial_balance