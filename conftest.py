import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.saucedemo.com"

USERS = {
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "locked":   {"username": "locked_out_user", "password": "secret_sauce"},
}


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        pg = context.new_page()
        yield pg
        context.close()
        browser.close()


@pytest.fixture
def logged_in_page(page):
    """Returns a page already logged in as standard_user."""
    page.goto(BASE_URL)
    page.fill("#user-name", USERS["standard"]["username"])
    page.fill("#password", USERS["standard"]["password"])
    page.click("#login-button")
    page.wait_for_url("**/inventory.html")
    return page
