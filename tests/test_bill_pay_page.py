from playwright.sync_api import expect, Page
from pages.bill_pay_page import BillPayPage
from pages.accounts_overview_page import AccountsOverviewPage

def test_bill_pay(logged_user, page: Page):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    account = accounts_overview_page.get_random_account()
    accounts_overview_page.show_td_list(account)
    account_initial_balance = accounts_overview_page.get_account_balance(account)
    bill_pay_page = BillPayPage(page)
    bill_pay_page.open()
    bill_pay_page.is_loaded()
    bill_pay_page.fill_payee_name("UserName")
    bill_pay_page.fill_address("Imaginary Address")
    bill_pay_page.fill_city("Imaginary City")
    bill_pay_page.fill_state("Imaginary State")
    bill_pay_page.fill_zip_code("123456789")
    bill_pay_page.fill_phone("987654321")
    bill_pay_page.fill_account("123123")
    bill_pay_page.fill_verify_account("123123")
    amount = 1
    bill_pay_page.fill_amount(str(amount))
    bill_pay_page.select_from_account(account)
    print("Quería seleccionar:", account)
    print("Quedó seleccionado:", bill_pay_page.from_account.input_value())
    bill_pay_page.click_send_payment()
    bill_pay_page.payment_finished_sign()
    accounts_overview_page.open()
    accounts_overview_page.is_loaded()
    accounts_overview_page.show_td_list(account)
    expect(page.get_by_text(account)).to_be_visible()
    account_final_balance = accounts_overview_page.get_account_balance(account)
    assert account_final_balance == account_initial_balance - amount
    

