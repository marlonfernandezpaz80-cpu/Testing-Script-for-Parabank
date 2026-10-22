from playwright.sync_api import Page, expect
import random
from .utils import wait_for

class OpenNewAccountPage():
    def __init__(self, page: Page):
        self.page = page
        self.right_panel = self.page.locator("div#rightPanel")
        self.title = self.right_panel.get_by_role("heading", name="Open New Account")
        self.account_type = self.right_panel.locator("select#type.input")
        self.account_selector = self.right_panel.locator("select#fromAccountId.input")
        self.account_options = self.account_selector.locator("option")
        self.open_new_account_button = self.right_panel.get_by_role("button", name="Open New Account")
        self.new_account_id = self.right_panel.locator("a#newAccountId")
        self.account_opened_sign = self.right_panel.get_by_role("heading", name="Account Opened!")

    def open(self):
        self.page.goto("openaccount.htm")

    def is_loaded(self):
        expect(self.title).to_be_visible()

    def select_account_type(self, value):
        self.account_type.select_option(value)

    def select_account(self, value):
        self.account_selector.select_option(value)

    def click_open_account(self):
        self.open_new_account_button.click()

    def account_opened(self):
        expect(self.account_opened_sign).to_be_visible()

    def get_new_account_number(self):
        account_id = self.new_account_id.inner_text()
        return account_id
    
    def get_random_account_options(self):
        wait_for(self.account_options)
        option = random.choice(self.account_options.all_inner_texts())
        return option 
