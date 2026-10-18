from playwright.sync_api import Page, expect
from .utils import wait_for

class TransferFundsPage():
    def __init__(self, page: Page):
        self.page = page
        self.right_panel = self.page.locator("div#rightPanel")
        self.title = self.right_panel.get_by_role("heading", name="Transfer Funds")
        self.amount_box = self.right_panel.locator("input#amount")
        self.from_account = self.right_panel.locator("select#fromAccountId.input")
        self.from_account_option = self.from_account.locator("option")
        self.to_account = self.right_panel.locator("select#toAccountId.input")
        self.to_account_option = self.to_account.locator("option")
        self.transfer_button = self.right_panel.get_by_role("button", name="Transfer")

    def open(self):
        self.page.goto("transfer.htm")
    def is_loaded(self):
        expect(self.title).to_be_visible()

    def set_amount(self, amount):
        self.amount_box.fill(str(amount))

    def source_account(self, account):
        self.from_account.select_option(str(account))

    def destination_account(self, account):
        self.to_account.select_option(str(account))

    def get_from_options(self):
        wait_for(self.from_account_option)
        return self.from_account_option.all_inner_texts()

    def get_to_options(self):
        wait_for(self.to_account_option)
        return self.to_account_option.all_inner_texts()
    
    def click_transfer(self):
        self.transfer_button.click()


    


