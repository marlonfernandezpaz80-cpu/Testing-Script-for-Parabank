from playwright.sync_api import expect, Page
from faker import Faker
from datetime import datetime, timedelta
import pytest

def wait_for(locator):
    expect(locator).not_to_have_count(0)

def generate_user(with_plus=True):
    fake = Faker("en_US")
    user = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.postcode(),
            "phone_number": fake.phone_number() if with_plus else fake.phone_number().replace("+", ""),
            "ssn": fake.ssn(),
            "username": fake.user_name(),
            "password": fake.password()
        }
    return user

def actualize_date(date):
    formated_date = datetime.strptime(date, "%m-%d-%Y")
    formated_date = formated_date + timedelta(days=1)
    final_date = datetime.strftime(formated_date, "%m-%d-%Y")
    return final_date

def get_all_dates(accounts, page: Page):
    from pages.accounts_overview_page import AccountsOverviewPage
    from pages.account_activity_page import AccountsActivityPage
    accounts_overview_page = AccountsOverviewPage(page)
    all_dates = []
    for account in accounts:
        accounts_overview_page.click_account(account)
        accounts_activity_page = AccountsActivityPage(page)
        accounts_activity_page.is_loaded()
        try:
            expect(accounts_activity_page.table_body).to_be_visible()
            dates = accounts_activity_page.get_lines_dates()
            for date in dates:
                all_dates.append(date)
        except AssertionError:
            expect(accounts_activity_page.no_transactions_sign).to_be_visible()
        accounts_overview_page.open()
        accounts_overview_page.is_loaded()
    return all_dates

def get_account_with_activity(accounts, page: Page):
    from pages.account_activity_page import AccountsActivityPage
    account_activity_page = AccountsActivityPage(page)
    account_activity = False
    target_account = ""
    for account in accounts:
        account_activity_page.open_account_activity(account)
        account_activity_page.is_loaded()
        account_activity_page.confirm_account(account)
        activity = account_activity_page.there_is_activity()
        if activity:
            target_account = account
            account_activity = True
            break
    if account_activity:
        return target_account
    else:
        pytest.skip("Ninguna cuenta del usuario tiene transacciones registradas")