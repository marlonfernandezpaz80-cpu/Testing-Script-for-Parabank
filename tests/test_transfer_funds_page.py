from playwright.sync_api import Page, expect
import random
from pages.transfer_funds_page import TransferFundsPage

def test_transfer_funds(page: Page, logged_user):
    logged_user.transfer_funds()
    transfer_funds_page = TransferFundsPage(page)
    transfer_funds_page.set_amount(3)
    from_options = transfer_funds_page.get_from_options()
    print(from_options)
    to_options = transfer_funds_page.get_to_options()
    print(to_options)
    from_account = random.choice(from_options)
    to_account = random.choice(to_options)
    transfer_funds_page.source_account(from_account)
    transfer_funds_page.destination_account(to_account)
    transfer_funds_page.click_transfer()