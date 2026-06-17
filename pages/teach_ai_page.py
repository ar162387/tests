"""Page object for the Teach AI section (data sources / file upload)."""

from playwright.sync_api import Page, expect


class TeachAIPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self) -> None:
        self.page.get_by_role("link", name="Teach AI").click()
        expect(
            self.page.locator('[data-test="teach-ai-data-sources-section"]')
        ).to_be_visible(timeout=30_000)

    def open_add_file(self) -> None:
        self.page.get_by_role("button", name="Add file").first.click()
        expect(
            self.page.locator('[data-test="teach-ai-add-file-container"]')
        ).to_be_visible()

    def upload_file(self, file_path: str) -> None:
        # The visible "Click to upload" control wraps a hidden <input type=file>.
        self.page.set_input_files("input[type=file]", file_path)
        # Wait for the upload to finish — the size label flips from "Uploading...".
        expect(self.page.locator('[data-test="file-size"]')).not_to_have_text(
            "Uploading...", timeout=60_000
        )

    def save(self) -> None:
        self.page.locator('[data-test="confirm-add-file-button"]').click()

    def add_file(self, file_path: str) -> None:
        """Full flow: open the Add file panel, upload, and save."""
        self.open_add_file()
        self.upload_file(file_path)
        self.save()

    def expect_file_in_sources(self, filename: str) -> None:
        sources = self.page.locator('[data-test="data-sources-list"]')
        item = sources.locator('[data-test="data-source-item"]', has_text=filename)
        expect(item.first).to_be_visible(timeout=30_000)
