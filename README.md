# SauceDemo – Frontend Test Automation

Automated test suite for [https://www.saucedemo.com](https://www.saucedemo.com)  
Built with **Playwright + pytest** (Python).

---

## Test Cases

| # | Test | Why it's essential |
|---|------|--------------------|
| TC-01 | Valid login redirects to inventory | Login is the entry point – if it breaks, nothing else works |
| TC-02 | Locked-out user sees clear error | Access control must be enforced with a meaningful message |
| TC-03 | Add/remove item updates cart badge | Visual feedback is critical so users know their action succeeded |
| TC-04 | Complete end-to-end checkout | The most business-critical flow – broken checkout = zero revenue |

---

## Tech Stack

- **Python 3.10+**
- **Playwright** – modern browser automation (Chromium)
- **pytest** – test runner
- **pytest-html** – HTML report generation

---

## Prerequisites

- Python 3.10 or newer installed
- `pip` available

---

## Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/saucedemo-tests.git
cd saucedemo-tests

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install chromium
```

---

## Running the Tests

### Run all tests
```bash
pytest tests/ -v
```

### Run a specific test class
```bash
pytest tests/ -v -k "TestLogin"
pytest tests/ -v -k "TestCart"
pytest tests/ -v -k "TestCheckout"
```

### Generate an HTML report
```bash
pytest tests/ -v --html=report.html --self-contained-html
```
Open `report.html` in your browser to view the results.

### Run in headed mode (watch the browser)
```bash
pytest tests/ -v --headed
```

---

## Project Structure

```
saucedemo-tests/
├── tests/
│   └── test_saucedemo.py   # All test cases
├── conftest.py              # Shared fixtures (browser setup, login helper)
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Test Users

Credentials are publicly available on the SauceDemo login page:

| User | Password | Notes |
|------|----------|-------|
| `standard_user` | `secret_sauce` | Normal user |
| `locked_out_user` | `secret_sauce` | Used for negative login test |

---

## Example Output

```
tests/test_saucedemo.py::TestLogin::test_valid_login_redirects_to_inventory PASSED
tests/test_saucedemo.py::TestLogin::test_locked_out_user_sees_error PASSED
tests/test_saucedemo.py::TestCart::test_add_item_updates_cart_badge PASSED
tests/test_saucedemo.py::TestCart::test_remove_item_hides_cart_badge PASSED
tests/test_saucedemo.py::TestCheckout::test_full_checkout_completes_successfully PASSED

5 passed in 12.34s
```
