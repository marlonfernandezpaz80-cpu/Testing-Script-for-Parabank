from playwright.sync_api import Page, expect


class UpdateProfilePage():
    def __init__(self, page: Page):
        self.page = page
        self.right_panel = self.page.locator("div#rightPanel")
        self.right_panel = self.page.locator("div#rightPanel")
        self.table = self.right_panel.locator("tbody")
        self.title = self.right_panel.get_by_role("heading", name="Update Profile")
        self.profile_updated_sign = self.page.get_by_role("heading", name="Profile Updated")
        self.first_name_textbox = self.table.locator('input[name="customer.firstName"]')
        self.last_name_textbox = self.table.locator('input[name="customer.lastName"]')
        self.address_textbox = self.table.locator('input[name="customer.address.street"]')
        self.city_textbox = self.table.locator('input[name="customer.address.city"]')
        self.state_textbox = self.table.locator('input[name="customer.address.state"]')
        self.zip_code_textbox = self.table.locator('input[name="customer.address.zipCode"]')
        self.phone_number_textbox = self.table.locator('input[name="customer.phoneNumber"]')
        self.update_profile_button = self.right_panel.get_by_role("button", name="Update Profile")


    def open(self):
        self.page.goto("updateprofile.htm")
    
    def is_loaded(self):
        expect(self.title).to_be_visible()
        expect(self.first_name_textbox).not_to_have_value("")

    def open(self):
        self.page.goto("updateprofile.htm")
        
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

    def click_update_profile_button(self):
        self.update_profile_button.click()

    def profile_was_updated(self):
        expect(self.profile_updated_sign).to_be_visible()