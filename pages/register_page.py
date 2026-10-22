from playwright.sync_api import Page, expect
import pytest

class RegisterPage():
    def __init__(self, page: Page):
        self.page = page
        self.right_panel = self.page.locator("div#rightPanel")
        self.title = self.right_panel.get_by_role("heading", name="Signing up is easy!")
        self.table = self.right_panel.locator("tbody")
        self.first_name_textbox = self.table.locator('input[name="customer.firstName"]')
        self.last_name_textbox = self.table.locator('input[name="customer.lastName"]')
        self.address_textbox = self.table.locator('input[name="customer.address.street"]')
        self.city_textbox = self.table.locator('input[name="customer.address.city"]')
        self.state_textbox = self.table.locator('input[name="customer.address.state"]')
        self.zip_code_textbox = self.table.locator('input[name="customer.address.zipCode"]')
        self.phone_number_textbox = self.table.locator('input[name="customer.phoneNumber"]')
        self.ssn_textbox = self.table.locator('input[name="customer.ssn"]')
        self.username_textbox = self.table.locator('input[name="customer.username"]')
        self.password_textbox = self.table.locator('input[name="customer.password"]')
        self.confirm_password_textbox = self.table.locator('input[name="repeatedPassword"]')
        self.register_button = self.table.get_by_role("button", name="Register")
        self.welcome_sign = self.page.get_by_role("heading").filter(has_text="Welcome")
        self.required_field_error = self.table.locator("span.error").filter(has_text="is required").first

    def fill_first_name(self, first_name):
        self.first_name_textbox.fill(first_name)

    def fill_last_name(self, last_name):
        self.last_name_textbox.fill(last_name)

    def fill_address(self, address):
        self.address_textbox.fill(address)

    def fill_city(self, city):
        self.city_textbox.fill(city)

    def fill_state(self, state):
        self.state_textbox.fill(state)

    def fill_zip_code(self, zip_code):
        self.zip_code_textbox.fill(zip_code)

    def fill_phone_number(self, phone_number):
        self.phone_number_textbox.fill(phone_number)

    def fill_ssn(self, ssn):
        self.ssn_textbox.fill(ssn)

    def fill_username(self, username):
        self.username_textbox.fill(username)

    def fill_password(self, password):
        self.password_textbox.fill(password)

    def fill_confirm_password(self, password):
        self.confirm_password_textbox.fill(password)

    def click_register(self):
        self.register_button.click()

    def is_loaded(self):
        expect(self.title).to_be_visible()

    def user_registered(self):
        expect(self.welcome_sign).to_be_visible()

    def user_not_registered(self):
        expect(self.welcome_sign).not_to_be_visible()
        expect(self.required_field_error).to_be_visible()

    