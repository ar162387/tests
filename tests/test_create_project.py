"""Flow 2: Create a project (AI Survey).

Uses the cached authenticated session (logged_in_page) so it doesn't
re-run the UI login. Opens the Add Project modal, picks the AI Survey
type, submits, and verifies we land on the survey/form editor.
"""

from playwright.sync_api import Page

from pages.create_project_page import CreateProjectPage


def test_create_ai_survey_project(logged_in_page: Page) -> None:
    create = CreateProjectPage(logged_in_page)
    create.create("survey")
    create.expect_survey_editor()
