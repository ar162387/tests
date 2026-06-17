"""Page object for the 'Add project' -> Create modal."""

import re

from playwright.sync_api import Page, expect

# Card labels map to non-obvious data-test ids, so keep the mapping in one place.
PROJECT_TYPE_RADIOS = {
    "user_test": "project-type-radio-usabilitytesting",  # AI User Test
    "interview": "project-type-radio-survey",             # AI Interview
    "survey": "project-type-radio-form",                  # AI Survey
    "poll": "project-type-radio-poll",                    # AI Poll
}


class CreateProjectPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self) -> None:
        self.page.locator('[data-test="add-project-button"]').click()
        expect(self.page.locator('[data-test="project-type-selector"]')).to_be_visible()

    def select_type(self, kind: str = "survey") -> None:
        radio = PROJECT_TYPE_RADIOS[kind]
        self.page.locator(f'[data-test="{radio}"]').click()

    def submit(self) -> None:
        # The footer button overflows below the fold on short viewports;
        # Playwright auto-scrolls it into view before clicking.
        self.page.locator('[data-test="create-project-button"]').click()

    def create(self, kind: str = "survey") -> None:
        """Full flow: open modal -> pick type -> submit."""
        self.open()
        self.select_type(kind)
        self.submit()

    def expect_survey_editor(self) -> None:
        """After creating an AI Survey we land on the project (form) editor."""
        expect(self.page).to_have_url(re.compile(r"/projects/new\?project-type=Form"))
        expect(self.page.locator('[data-test="project-page"]')).to_be_visible(
            timeout=30_000
        )
        expect(self.page.locator('[data-test="project-form"]')).to_be_visible()
