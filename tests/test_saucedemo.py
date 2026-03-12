"""
SauceDemo - Frontend Automation Tests
======================================
Test cases cover the 4 most critical user flows:
  TC-01  Login – valid credentials
  TC-02  Login – locked-out user (negative)
  TC-03  Add to cart & verify cart badge
  TC-04  Complete full checkout flow

Why these flows?
  Authentication is the entry point to the entire application – without it
  nothing else works.  The cart and checkout flows represent the core business
  value of an e-shop: if a user cannot buy a product, the application fails
  its primary purpose.
"""

import pytest

BASE_URL = "https://www.saucedemo.com"


# ─────────────────────────────────────────────────────────────────────────────
# TC-01  Successful login with valid credentials
# ─────────────────────────────────────────────────────────────────────────────
class TestLogin:
    """
    Why essential:
        Login is the gateway to the whole application.  A broken login means
        zero users can access any feature.  This is always the first test that
        must pass before anything else is verified.
    """

    def test_valid_login_redirects_to_inventory(self, page):
        """Standard user can log in and reaches the product page."""
        page.goto(BASE_URL)

        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")

        assert "/inventory.html" in page.url, (
            "After valid login the user should be redirected to /inventory.html"
        )
        assert page.is_visible(".inventory_list"), (
            "Product list should be visible after login"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # TC-02  Locked-out user receives a clear error message
    # ─────────────────────────────────────────────────────────────────────────
    def test_locked_out_user_sees_error(self, page):
        """
        Why essential:
            The application must not silently fail or show a generic error for
            locked accounts.  Users (and support teams) need a clear, actionable
            message.  This also verifies that access control is enforced.
        """
        page.goto(BASE_URL)

        page.fill("#user-name", "locked_out_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")

        error = page.locator("[data-test='error']")
        assert error.is_visible(), "Error message container should be visible"

        error_text = error.inner_text()
        assert "locked out" in error_text.lower(), (
            f"Error should mention 'locked out', got: '{error_text}'"
        )


# ─────────────────────────────────────────────────────────────────────────────
# TC-03  Add a product to the cart – badge counter updates
# ─────────────────────────────────────────────────────────────────────────────
class TestCart:
    """
    Why essential:
        Adding items to the cart is the first step of every purchase.  If the
        cart counter does not update the user has no visual confirmation that
        their action succeeded, leading to confusion or duplicate orders.
    """

    def test_add_item_updates_cart_badge(self, logged_in_page):
        page = logged_in_page

        # Cart should start empty
        assert not page.is_visible(".shopping_cart_badge"), (
            "Cart badge should not be visible when cart is empty"
        )

        # Add the first product on the page
        page.locator(".btn_primary.btn_inventory").first.click()

        badge = page.locator(".shopping_cart_badge")
        assert badge.is_visible(), "Cart badge should appear after adding an item"
        assert badge.inner_text() == "1", (
            f"Cart badge should show '1', got '{badge.inner_text()}'"
        )

    def test_remove_item_hides_cart_badge(self, logged_in_page):
        page = logged_in_page

        # Add then remove
        add_btn = page.locator(".btn_primary.btn_inventory").first
        add_btn.click()
        page.locator(".btn_secondary.btn_inventory").first.click()

        assert not page.is_visible(".shopping_cart_badge"), (
            "Cart badge should disappear after removing the only item"
        )


# ─────────────────────────────────────────────────────────────────────────────
# TC-04  Complete end-to-end checkout flow
# ─────────────────────────────────────────────────────────────────────────────
class TestCheckout:
    """
    Why essential:
        The checkout flow is the most business-critical path in any e-commerce
        application.  Even if all other features work perfectly, a broken
        checkout means zero revenue.  End-to-end coverage here catches
        regressions across multiple integrated components (cart → form →
        order summary → confirmation).
    """

    def test_full_checkout_completes_successfully(self, logged_in_page):
        page = logged_in_page

        # 1. Add a product
        page.locator(".btn_primary.btn_inventory").first.click()

        # 2. Open cart
        page.click(".shopping_cart_link")
        page.wait_for_url("**/cart.html")
        assert page.is_visible(".cart_item"), "Cart page should contain the added item"

        # 3. Proceed to checkout
        page.click("[data-test='checkout']")
        page.wait_for_url("**/checkout-step-one.html")

        # 4. Fill in customer info
        page.fill("[data-test='firstName']", "Jan")
        page.fill("[data-test='lastName']", "Novak")
        page.fill("[data-test='postalCode']", "01001")
        page.click("[data-test='continue']")
        page.wait_for_url("**/checkout-step-two.html")

        # 5. Verify order summary is present
        assert page.is_visible(".cart_item"), "Order summary should show the item"
        assert page.is_visible(".summary_total_label"), "Total price label should be visible"

        # 6. Finish the order
        page.click("[data-test='finish']")
        page.wait_for_url("**/checkout-complete.html")

        confirmation = page.locator(".complete-header")
        assert confirmation.is_visible(), "Confirmation header should be visible"
        assert "thank you" in confirmation.inner_text().lower(), (
            f"Confirmation text should contain 'Thank you', got: '{confirmation.inner_text()}'"
        )
