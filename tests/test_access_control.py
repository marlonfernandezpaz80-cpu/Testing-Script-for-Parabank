from playwright.sync_api import Page, expect
import pytest
protected_pages = ["overview.htm", "billpay.htm", "findtrans.htm", "openaccount.htm", "requestloan.htm", "transfer.htm", "updateprofile.htm"]


@pytest.mark.negative
@pytest.mark.parametrize("route", protected_pages)
def test_acces_control(page: Page, route):
    page.goto(route)
    expect(page.get_by_role("heading", name="Error!")).to_be_visible()
    expect(page.get_by_text("An internal error has occurred and has been logged").first).to_be_visible()