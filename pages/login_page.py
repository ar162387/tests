"""Page object for the AuthKit login flow."""

import re

from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto(self) -> None:
        # Visiting the app while unauthenticated redirects to the AuthKit login.
        self.page.goto(self.base_url)

    def login(self, email: str, password: str) -> None:
        # AuthKit is a two-step form: email -> Continue -> password -> Sign in.
        self.page.get_by_role("textbox", name="Email").fill(email)
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()

    def expect_logged_in(self) -> None:
        # Back on the app domain with the project dashboard control present.
        expect(self.page).to_have_url(re.compile(r"theysaid\.io"))
        expect(self.page.locator('[data-test="add-project-button"]')).to_be_visible(
            timeout=30_000
        )
