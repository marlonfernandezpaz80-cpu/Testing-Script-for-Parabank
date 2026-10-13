from playwright.sync_api import expect, Page

class BillPayPage():
    def __init__(self, page: Page):
        self.page = page
        self.right_panel = self.page.locator("div#rightPanel")
        self.title = self.right_panel.get_by_role("heading", name="Bill Payment Service")
        self.form_table = self.right_panel.locator("table.form2")
        self.payee_name = self.form_table.locator("input[name='payee.name']")
        self.address =self.form_table.locator("input[name='payee.address.street']")
        self.city = self.form_table.locator("input[name='payee.address.city']")
        self.state = self.form_table.locator("input[name='payee.address.state']")
        self.zip_code = self.form_table.locator("input[name='payee.address.zipCode']")
        self.phone_number = self.form_table.locator("input[name='payee.phoneNumber']")
        self.account = self.form_table.locator("input.input[name='payee.accountNumber']")
        self.verify_account = self.form_table.locator("input[name='verifyAccount']")
        self.amount = self.form_table.locator("input[name='amount']")
        self.from_account = self.form_table.locator("select.input[name='fromAccountId']")
        self.send_payment_button = self.form_table.get_by_role("button", name="Send Payment")
        self.bill_payment_complete = self.right_panel.get_by_role("heading", name="Bill Payment Complete")

    def open(self):
        self.page.goto("billpay.htm")

    def is_loaded(self):
        expect(self.title).to_be_visible()

    def fill_payee_name(self, name):
        self.payee_name.fill(name)

    def fill_address(self, address):
        self.address.fill(address)

    def fill_city(self, city):
        self.city.fill(city)

    def fill_state(self, state):
        self.state.fill(state)

    def fill_zip_code(self, zip_code):
        self.zip_code.fill(zip_code)

    def fill_phone(self, phone):
        self.phone_number.fill(phone)

    def fill_account(self, account):
        self.account.fill(account)

    def fill_verify_account(self, account):
        self.verify_account.fill(account)

    def fill_amount(self, amount):
        self.amount.fill(amount)

    def select_from_account(self, account):
        self.from_account.select_option(account)

    def click_send_payment(self):
        self.send_payment_button.click()

    def payment_finished_sign(self):
        expect(self.bill_payment_complete).to_be_visible()