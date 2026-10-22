from playwright.sync_api import Page, expect
from .utils import wait_for, parse_amount, generate_columns
from random import choice 

class AccountsOverviewPage():
    def __init__(self, page: Page):
        self.page = page
        self.right_panel = self.page.locator("div#rightPanel")
        self.title = self.right_panel.get_by_role("heading", name="Accounts Overview")
        self.table = self.right_panel.locator("table#accountTable")
        self.accounts_numbers = self.table.locator("a")
        self.table_body = self.table.locator("tbody")
        self.table_line = self.table_body.locator("tr")
        self.total = self.table_line.filter(has_text="Total")

    def open(self):
        self.page.goto("overview.htm")

    def is_loaded(self):
        expect(self.title).to_be_visible()
        expect(self.total).to_be_visible()

    def get_accounts_list(self):
        wait_for(self.accounts_numbers)
        accounts_list = self.accounts_numbers.all_inner_texts()
        return accounts_list

    def get_random_account(self):
        accounts_list = self.get_accounts_list()
        account = choice(accounts_list)
        return account

    def click_account(self, account):
        self.accounts_numbers.filter(has_text=account).click()

    def get_account_balance(self, account):
        line = self.table_line.filter(has_text=account)
        columns = generate_columns(line)
        return parse_amount(columns[1])