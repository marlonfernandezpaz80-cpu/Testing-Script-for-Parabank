from playwright.sync_api import Page, expect
import pytest

def get_all_dates(account, page: Page):
    from pages.accounts_overview_page import AccountsOverviewPage
    from pages.account_activity_page import AccountsActivityPage
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.open()
    accounts_overview_page.is_loaded()
    all_dates = set()
    accounts_overview_page.click_account(account)
    accounts_activity_page = AccountsActivityPage(page)
    accounts_activity_page.is_loaded()
    try:
        expect(accounts_activity_page.table_body).to_be_visible()
        dates = accounts_activity_page.get_lines_dates()
        for date in dates:
            all_dates.add(date)
    except AssertionError:
        expect(accounts_activity_page.no_transactions_sign).to_be_visible()
    accounts_overview_page.open()
    accounts_overview_page.is_loaded()
    return list(all_dates)

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