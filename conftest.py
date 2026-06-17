import os
from pathlib import Path
from typing import Dict, Any

import pytest
from playwright.sync_api import Browser, BrowserType, Page

# Use the pre-installed browser — no network download needed
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", r"D:\playwright-browsers")


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: Dict[str, Any]) -> Dict[str, Any]:
    """Launch the browser maximized so it uses the screen's native resolution."""
    return {
        **browser_type_launch_args,
        "args": [*browser_type_launch_args.get("args", []), "--start-maximized"],
    }

from config import settings  # noqa: E402
from pages.login_page import LoginPage  # noqa: E402

# Where the authenticated session is cached between tests
_AUTH_DIR = Path(__file__).parent / ".auth"
_STORAGE_STATE = _AUTH_DIR / "state.json"


@pytest.fixture(scope="session")
def app_settings():
    """Expose BASE_URL / credentials to any test that needs them."""
    assert settings.email and settings.password, (
        "TEST_EMAIL / TEST_PASSWORD missing — copy .env.example to .env"
    )
    return settings


@pytest.fixture(scope="session")
def auth_storage(browser: Browser, app_settings) -> str:
    """Log in once per session and cache the storage state to disk.

    The login flow itself is exercised by tests/test_login.py; here we only
    need a valid authenticated session so the other flows can skip the UI login.
    """
    _AUTH_DIR.mkdir(exist_ok=True)
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    login = LoginPage(page, app_settings.base_url)
    login.goto()
    login.login(app_settings.email, app_settings.password)
    login.expect_logged_in()

    context.storage_state(path=str(_STORAGE_STATE))
    context.close()
    return str(_STORAGE_STATE)


@pytest.fixture
def logged_in_page(browser: Browser, auth_storage: str, app_settings) -> Page:
    """A fresh page that is already authenticated, landing on the app."""
    context = browser.new_context(
        storage_state=auth_storage,
        no_viewport=True,
    )
    page = context.new_page()
    page.goto(app_settings.base_url)
    yield page
    context.close()
