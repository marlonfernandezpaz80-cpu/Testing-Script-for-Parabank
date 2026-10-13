from playwright.sync_api import Page, expect
from pages.accounts_overview_page import AccountsOverviewPage
from pages.account_activity_page import AccountsActivityPage

def test_account_activity(logged_user, page: Page):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    account = accounts_overview_page.get_random_account()
    accounts_overview_page.click_account(account)
    account_activity_page = AccountsActivityPage(page)
    account_activity_page.is_loaded()
    account_activity_page.confirm_account(account)    
    chosen_date = account_activity_page.get_random_date()
    chosen_type = account_activity_page.get_random_type()
    account_activity_page.select_month(chosen_date)
    account_activity_page.select_type(chosen_type)
    account_activity_page.click_go()
    account_activity_page.verificate_filter(chosen_date, chosen_type)

