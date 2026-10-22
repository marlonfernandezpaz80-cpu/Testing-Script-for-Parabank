from playwright.sync_api import Page, expect
from pages.accounts_overview_page import AccountsOverviewPage
from pages.account_activity_page import AccountsActivityPage
from pages.find_transactions_page import FindTransactionsPage
from pages.transaction_details_page import TransactionDetailsPage
from random import choice
from datetime import datetime, timedelta
from pages.utils import add_one_day, substract_one_day
from .helpers import get_all_dates, get_account_with_activity
import pytest

@pytest.mark.regression
def test_find_by_transaction_id(logged_user, page: Page):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    accounts_list = accounts_overview_page.get_accounts_list()
    account = get_account_with_activity(accounts_list, page)
    account_activity_page = AccountsActivityPage(page)
    account_activity_page.is_loaded()
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
    find_transactions_page.transaction_results_are_loaded()
    find_transactions_page.click_transaction_filtered_by_id()
    transaction_details_page = TransactionDetailsPage(page)
    transaction_details_page.is_loaded()
    transaction_details_page.verificate_dats(transaction_id, transaction_date, transaction_description, transaction_type, transaction_amount)

@pytest.mark.regression
def test_find_by_date(logged_user, page: Page):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    accounts = accounts_overview_page.get_accounts_list()
    account = get_account_with_activity(accounts, page)
    accounts_overview_page.open()
    accounts_overview_page.is_loaded()
    dates = get_all_dates(account, page)  
    actualized_dates = []
    for date in dates:
        actualized_date = add_one_day(date)
        actualized_dates.append(actualized_date)

    target_date = choice(actualized_dates)
    find_transactions_page = FindTransactionsPage(page)
    find_transactions_page.open()
    find_transactions_page.is_loaded()
    find_transactions_page.select_account(account)
    find_transactions_page.find_by_transaction_date(target_date)
    find_transactions_page.transaction_results_are_loaded()
    result_dates = find_transactions_page.get_lines_dates()
    actualized_target_date = substract_one_day(target_date)
    dates_are_right = True
    for date in result_dates:
        if date != actualized_target_date:
            dates_are_right = False
            break
    assert dates_are_right

@pytest.mark.regression
def test_find_by_date_range(logged_user, page: Page):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    accounts = accounts_overview_page.get_accounts_list()
    account = get_account_with_activity(accounts, page)
    all_dates = get_all_dates(account, page)
    dates_dict = {}
    for date in all_dates:
        formated_date = datetime.strptime(date, "%m-%d-%Y")
        dates_dict[date] = formated_date
    latest_date =""
    earliest_dates = []
    for key, value in dates_dict.items():
        if not latest_date:
         latest_date = key
        else:
            if value > dates_dict[latest_date]:
             latest_date = key
    if len(all_dates) > 1:
        new_dates = [d for d in all_dates if d != latest_date]
        final_date = choice(new_dates)
        for key, value in dates_dict.items():
            if value < dates_dict[latest_date]:
                earliest_dates.append(key)
        starting_date = choice(earliest_dates)
    else:
        final_date = all_dates[0]
        starting_date = all_dates[0]
    starting_date = add_one_day(starting_date)
    final_date = add_one_day(final_date)
    find_transactions_page = FindTransactionsPage(page)
    find_transactions_page.open()
    find_transactions_page.is_loaded()
    find_transactions_page.find_by_transaction_period(starting_date, final_date)
    starting_date = substract_one_day(starting_date)
    final_date = substract_one_day(final_date)
    find_transactions_page.transaction_results_are_loaded()
    result_dates = find_transactions_page.get_lines_dates()
    right_dates = True
    for date in result_dates:
        formated_date = datetime.strptime(date, "%m-%d-%Y")
        starting_formated_date = datetime.strptime(starting_date, "%m-%d-%Y")
        final_formated_date = datetime.strptime(date, "%m-%d-%Y")
        if formated_date < starting_formated_date or formated_date > final_formated_date:
            right_dates = False
            break
    assert right_dates

@pytest.mark.regression
def test_find_by_amount(page: Page, logged_user):
    logged_user.accounts_overview()
    accounts_overview_page = AccountsOverviewPage(page)
    accounts_overview_page.is_loaded()
    accounts_list = accounts_overview_page.get_accounts_list()
    account = get_account_with_activity(accounts_list, page)
    accounts_activity_page = AccountsActivityPage(page)
    accounts_activity_page.open_account_activity(account)
    accounts_activity_page.is_loaded()
    accounts_activity_page.confirm_account(account)
    amounts = accounts_activity_page.get_amounts_list()
    target_amount = choice(amounts)
    find_transactions_page = FindTransactionsPage(page)
    find_transactions_page.open()
    find_transactions_page.is_loaded()
    find_transactions_page.select_account(account)
    find_transactions_page.find_by_transaction_amount(str(target_amount))
    result_amounts = find_transactions_page.get_lines_amounts()
    assert result_amounts
    assert all(amount == target_amount for amount in result_amounts)


@pytest.mark.negative
def test_find_by_random_id(page: Page, logged_user):
    logged_user.find_transactions()
    find_transactions_page = FindTransactionsPage(page)
    find_transactions_page.open()
    find_transactions_page.is_loaded()
    find_transactions_page.find_by_transaction_id("999999")
    find_transactions_page.transaction_results_are_loaded()
    expect(find_transactions_page.table_body).not_to_be_visible()