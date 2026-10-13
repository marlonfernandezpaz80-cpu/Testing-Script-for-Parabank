from playwright.sync_api import Page, expect
from random import choice

class RequestLoanPage():
    def __init__(self, page: Page):
        self.page = page
        self.right_panel = self.page.locator("div#rightPanel")
        self.title = self.right_panel.get_by_role("heading", name="Apply for a Loan")
        self.table = self.right_panel.locator("tbody")
        self.amount_textbox = self.table.locator("#amount.input")
        self.down_payment_textbox = self.table.locator("#downPayment.input")
        self.from_account_selector = self.table.locator("#fromAccountId.input")
        self.available_accounts = self.from_account_selector.locator("option")
        self.apply_now_button = self.table.get_by_role("button", name="Apply Now")
        self.loan_request_processed_sign = self.right_panel.get_by_role("heading", name="Loan Request Processed")
        self.loan_status = self.right_panel.locator("#loanStatus")
        self.new_account = self.right_panel.locator("a#newAccountId")

    def open(self):
        self.page.goto("requestloan.htm")

    def is_loaded(self):
        expect(self.title).to_be_visible()
        expect(self.from_account_selector).to_be_visible()

    def get_an_account(self):
        expect(self.from_account_selector).to_be_visible()
        account = choice(self.available_accounts.all_inner_texts())
        return account

    def select_account(self, account):
        self.from_account_selector.select_option(account)

    def fill_amount(self, amount):
        self.amount_textbox.fill(amount)

    def fill_down_payment(self, amount):
        self.down_payment_textbox.fill(amount)

    def click_apply_now(self):
        self.apply_now_button.click()

    def loan_processed(self):
        expect(self.loan_request_processed_sign).to_be_visible()

    def loan_is_approved(self):
        expect(self.loan_status).to_contain_text("Approved")

    def get_new_account_id(self):
        return self.new_account.inner_text()
    

