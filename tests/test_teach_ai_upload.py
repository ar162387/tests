"""Flow 3: Upload a document in Teach AI.

Reuses the cached authenticated session, navigates to Teach AI, uploads
the sample .docx, saves it, and verifies it shows up as a data source.
"""

from playwright.sync_api import Page

from pages.teach_ai_page import TeachAIPage


def test_upload_document_to_teach_ai(logged_in_page: Page, app_settings) -> None:
    teach_ai = TeachAIPage(logged_in_page)
    teach_ai.goto()
    teach_ai.add_file(app_settings.sample_doc)
    teach_ai.expect_file_in_sources("NMR PART 2.docx")
