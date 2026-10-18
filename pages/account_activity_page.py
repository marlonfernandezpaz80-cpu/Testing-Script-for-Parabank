from playwright.sync_api import Page, expect
from datetime import datetime
from random import choice

class AccountsActivityPage ():
    def __init__(self, page: Page):
        self.page = page
        self.right_panel = self.page.locator("div#rightPanel")
        self.title = self.right_panel.get_by_role("heading", name="Account Details")
        self.account_number = self.right_panel.locator("#accountId")
        self.account_type = self.right_panel.locator("#accountType")
        self.account_balance = self.right_panel.locator("#balance")
        self.account_available_balance = self.right_panel.locator("#availableBalance")
        self.month_seletor = self.right_panel.locator("#month")
        self.type_selector = self.right_panel.locator("#transactionType")
        self.go_button = self.right_panel.get_by_role("button", name="Go")
        self.no_transactions_sign = self.right_panel.locator("#noTransactions")
        self.transaction_table = self.right_panel.locator("#transactionTable")
        self.table_body = self.transaction_table.locator("tbody")
        self.table_line = self.table_body.locator("tr")
        self.months_values = self.month_seletor.locator("option")
        self.types_values = self.type_selector.locator("option")

    def open_account_activity(self, account):
        self.page.goto(f"activity.htm?id={account}")

    def is_loaded(self):
        expect(self.title).to_be_visible()
        expect(self.table_line.first.locator("td").first).not_to_have_text("")

    def confirm_account(self, account):
        expect(self.account_number).to_contain_text(account)

    def there_is_activity(self):
        try:
            expect(self.transaction_table).to_be_visible()
            lines_count = len(self.table_line.all_inner_texts())
            if lines_count >= 2:
                return True
            else:
                return False
        except:
            expect(self.no_transactions_sign).to_be_visible()
            return False

    def get_lines_list(self):
        return self.table_line.all_inner_texts()

    def get_lines_dates(self):
        lines = self.get_lines_list()
        dates = []
        for line in lines:
            columns = line.split("\t")
            dates.append(columns[0])
        return dates

    def get_a_line_index(self):
        lines = self.table_line.all_inner_texts()
        lines_len = len(lines)
        line_index = choice(range(lines_len))
        return line_index

    def click_transaction(self, line_index):
        self.table_line.nth(line_index).get_by_role("link").click()

    def get_account_type(self):
        expect(self.account_type).not_to_have_text("")
        return self.account_type.inner_text().upper()

    def click_go(self):
        self.go_button.click()
        self.page.wait_for_timeout(1000)

    def select_month(self, month= "all"):
        self.month_seletor.select_option(month.capitalize())

    def select_type(self, type= "all"):
        self.type_selector.select_option(type.capitalize())

    def get_random_date(self):
        dates = self.months_values.all_inner_texts()
        chosen_date = choice(dates)
        return chosen_date

    def get_random_type(self):
        types = self.types_values.all_inner_texts()
        chosen_type = choice(types)
        return chosen_type

    def verificate_filter(self, month, type):
        try:
            expect(self.transaction_table).to_be_visible()
        except AssertionError:
            expect(self.no_transactions_sign).to_be_visible()
        if month != "All":
            selected_month = month[:3]
            selected_month = selected_month.lower()
            formated_selected_month = datetime.strptime(selected_month, f"%b")
            if self.transaction_table.is_visible():
                dates = []
                debits = []
                credits = []
                for line in self.table_line.all_inner_texts():
                    columns = line.split("\t")
                    dates.append(columns[0])
                    if columns[2] and not columns[3]:  
                        debits.append(columns[2][1::])
                    if not columns[2] and columns[3]: 
                        credits.append(columns[3][1::])

                for date in dates:
                    transaction_date = datetime.strptime(date, f"%m-%d-%Y")
                    assert transaction_date.month == formated_selected_month.month
                if type == "Debit":
                    assert not credits
                elif type == "Credit":
                    assert not debits
        else:
            if self.table.is_visible():
                if type == "All":
                    pass
                else:
                    debits = []
                    credits = []
                    for line in self.table_line.all_inner_texts():
                        columns = line.split("\t")
                        if columns[2] and not columns[3]:  
                            debits.append(columns[2][1::])
                        if not columns[2] and columns[3]: 
                            credits.append(columns[3][1::])
                    if type == "Credit":
                        assert not debits
                    elif type == "Debit":
                        assert not credits
