"""Flow 1: Log in.

Exercises the full AuthKit login from a clean (unauthenticated) browser.
"""

from playwright.sync_api import Page

from pages.login_page import LoginPage


def test_login(page: Page, app_settings) -> None:
    login = LoginPage(page, app_settings.base_url)
    login.goto()
    login.login(app_settings.email, app_settings.password)
    login.expect_logged_in()
