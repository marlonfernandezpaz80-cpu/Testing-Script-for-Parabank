from playwright.sync_api import Page, expect

class MenuComponent():
    def __init__(self, page: Page):
        self.page = page
        self.left_panel = self.page.locator("div#leftPanel")
        self.open_new_account_button = self.left_panel.get_by_role("link", name="Open New Account")
        self.accounts_overview_button = self.left_panel.get_by_role("link", name="Accounts Overview")
        self.transfer_funds_button = self.left_panel.get_by_role("link", name="Transfer Funds")
        self.bill_pay_button = self.left_panel.get_by_role("link", name="Bill Pay")
        self.find_transactions_button = self.left_panel.get_by_role("link", name="Find Transactions")
        self.update_contact_info_button = self.left_panel.get_by_role("link", name="Update Contact Info")
        self.request_loan_button = self.left_panel.get_by_role("link", name="Request Loan")
        self.log_out_button = self.left_panel.get_by_role("link", name="Log Out")
        self.title = self.left_panel.get_by_role("heading", name="Account Services")
        self.error_sign = self.page.get_by_role("heading", name="Error!")

    def is_loaded(self):
        expect(self.title).to_be_visible()

    def open_new_account(self):
        self.open_new_account_button.click()

    def accounts_overview(self):
        self.accounts_overview_button.click()

    def transfer_funds(self):
        self.transfer_funds_button.click()

    def bill_pay(self):
        self.bill_pay_button.click()

    def find_transactions(self):
        self.find_transactions_button.click()

    def update_contact_info(self):
        self.update_contact_info_button.click()

    def request_loan(self):
        self.request_loan_button.click()

    def log_out(self):
        self.log_out_button.click()
