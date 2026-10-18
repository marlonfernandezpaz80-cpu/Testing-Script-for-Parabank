from playwright.sync_api import Page, expect


class LoginPage():
    def __init__(self, page: Page):
        self.page = page
        self.login_panel = page.locator("#loginPanel")
        self.username_textbox = self.login_panel.locator('input[name="username"]')
        self.password_textbox = self.login_panel.locator('input[name="password"]')
        self.login_button = self.login_panel.get_by_role("button", name="Log In")
        self.title = self.page.get_by_role("heading", name="Customer Login")
        self.register_link = self.page.get_by_role("link", name="Register")
        self.error_sign = self.page.get_by_role("heading", name="Error!")
        
    def open(self):
        self.page.goto("index.htm")

    def fill_username(self, username):
        self.username_textbox.fill(username)

    def fill_password(self, password):
        self.password_textbox.fill(password)

    def click_login(self):
        self.login_button.click()

    def is_loaded(self):
        expect(self.title).to_be_visible()

    def click_register(self):
        self.register_link.click()

        