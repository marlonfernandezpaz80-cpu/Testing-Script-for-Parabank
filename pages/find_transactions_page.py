from playwright.sync_api import Page, expect
from .utils import parse_amount, generate_columns

class FindTransactionsPage():
    def __init__(self, page: Page):
        self.page = page
        self.right_panel = self.page.locator("div#rightPanel")
        self.title = self.right_panel.get_by_role("heading", name="Find Transactions")
        self.account_input = self.right_panel.locator("select#accountId")
        self.transaction_id_input = self.right_panel.locator("input#transactionId")
        self.find_transactions_by_id_button = self.right_panel.locator("#findById")
        self.transaction_date_input = self.right_panel.locator("input#transactionDate")
        self.find_transactions_by_date_button = self.right_panel.locator("#findByDate")
        self.transaction_from_date_input = self.right_panel.locator("input#fromDate")
        self.transaction_to_date_input = self.right_panel.locator("input#toDate")
        self.find_transactions_by_date_range_button = self.right_panel.locator("#findByDateRange")
        self.transaction_amount_input = self.right_panel.locator("input#amount")
        self.find_transactions_by_amount_button = self.right_panel.locator("#findByAmount")
        self.transaction_results_title = self.right_panel.get_by_role("heading", name="Transaction Results")
        self.table = self.right_panel.locator("table#transactionTable")
        self.table_body = self.table.locator("tbody")
        self.table_line = self.table_body.locator("tr")

    def open(self):
        self.page.goto("findtrans.htm")

    def is_loaded(self):
        expect(self.title).to_be_visible()

    def transaction_results_are_loaded(self):
        expect(self.table).to_be_visible()
        expect(self.transaction_results_title).to_be_visible()

    def select_account(self, account):
        self.account_input.select_option(account)

    def find_by_transaction_id(self, trans_id):
        self.transaction_id_input.fill(trans_id)
        self.find_transactions_by_id_button.click()

    def find_by_transaction_date(self, trans_date):
        self.transaction_date_input.fill(trans_date)
        self.find_transactions_by_date_button.click()

    def find_by_transaction_period(self, trans_from_date, trans_to_date):
        self.transaction_from_date_input.fill(trans_from_date)
        self.transaction_to_date_input.fill(trans_to_date)
        self.find_transactions_by_date_range_button.click()

    def find_by_transaction_amount(self, amount):
        self.transaction_amount_input.fill(amount)
        self.find_transactions_by_amount_button.click()

    def click_transaction_filtered_by_id(self):
        self.table_line.get_by_role("link").click()

    def get_lines_list(self):
        expect(self.table_body.get_by_role("link").first).to_be_visible()
        lines_list = self.table_line.all_inner_texts()
        return lines_list

    def get_lines_dates(self):
        dates = []
        for line in self.get_lines_list():
            columns = generate_columns(line)
            dates.append(columns[0])
        return dates

    def get_lines_amounts(self):
        amounts = set()
        for line in self.get_lines_list():
            _, _, debit, credit = generate_columns(line)
            amounts.add(parse_amount(debit or credit))
        return list(amounts)