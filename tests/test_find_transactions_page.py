from playwright.sync_api import Page, expect
from pages.accounts_overview_page import AccountsOverviewPage
from pages.account_activity_page import AccountsActivityPage
from pages.find_transactions_page import FindTransactionsPage
from pages.transaction_details_page import TransactionDetailsPage
from random import choice
from datetime import datetime
from pages.utils import actualize_date, get_all_dates, get_account_with_activity
'''
def test_find_by_transaction_id(logged_user, page: Page):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    accounts_list = accounts_overview_page.get_accounts_list()
    account = get_account_with_activity(accounts_list, page)
    account_activity_page = AccountsActivityPage(page)
    line_index = account_activity_page.get_a_line_index()
    account_activity_page.click_transaction(line_index)
    transaction_details_page = TransactionDetailsPage(page)
    transaction_details_page.is_loaded()
    transaction_id = transaction_details_page.get_transaction_id()
    transaction_date = transaction_details_page.get_transaction_date()
    transaction_description = transaction_details_page.get_transaction_description()
    transaction_amount = transaction_details_page.get_transaction_amount()
    transaction_type = transaction_details_page.get_transaction_type()
    find_transactions_page = FindTransactionsPage(page)
    find_transactions_page.open()
    find_transactions_page.is_loaded()
    find_transactions_page.select_account(account)
    find_transactions_page.find_by_transaction_id(transaction_id)
    find_transactions_page.click_transaction_filtered_by_id()
    transaction_details_page = TransactionDetailsPage(page)
    transaction_details_page.is_loaded()
    transaction_details_page.verificate_dats(transaction_id, transaction_date, transaction_description, transaction_type, transaction_amount)

def test_find_by_date(logged_user, page: Page):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    accounts = accounts_overview_page.get_accounts_list()
    dates = get_all_dates(accounts, page)  
    all_dates = []
    for date in dates:
        actualized_date = actualize_date(date)
        all_dates.append(actualized_date)

    target_date = choice(all_dates)
    account = get_account_with_activity(accounts, page)
    find_transactions_page = FindTransactionsPage(page)
    find_transactions_page.open()
    find_transactions_page.is_loaded()
    find_transactions_page.select_account(account)
    find_transactions_page.find_by_transaction_date(target_date)
    find_transactions_page.table_is_loaded()
    lines = find_transactions_page.get_lines_list()
    result_dates = find_transactions_page.get_lines_dates(lines)
    result_dates = set(result_dates)
    assert len(result_dates) == 1
'''
def test_find_by_date_range(logged_user, page: Page):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    accounts = accounts_overview_page.get_accounts_list()
    all_dates = get_all_dates(accounts, page)
    all_dates = set(all_dates)
    all_dates = list(all_dates)
    dates = []
    for date in all_dates:
       actualized_date = actualize_date(date)
       dates.append(actualized_date)
    dates_dict = {}
    for date in dates:
        formated_date = datetime.strptime(date, "%m-%d-%Y")
        dates_dict[date] = formated_date
    latest_date =""
    earliest_dates = []
    for key, value in dates_dict.items():
        if latest_date == "":
         latest_date = key
        else:
            if value > dates_dict[latest_date]:
             latest_date = key
    if len(dates) > 1:
        new_dates = [d for d in dates if d != latest_date]
        final_date = choice(new_dates)
        for key, value in dates_dict.items():
            if value < dates_dict[latest_date]:
                earliest_dates.append(key)
        starting_date = choice(earliest_dates)
    else:
        final_date = dates[0]
        starting_date = dates[0]

    #Fin del flujo
    find_transactions_page = FindTransactionsPage(page)
    find_transactions_page.open()
    find_transactions_page.is_loaded()
    find_transactions_page.find_by_transaction_period(starting_date, final_date)
    