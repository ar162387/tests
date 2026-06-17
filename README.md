# TheySaid — Playwright E2E Tests (Python)

📹 **Demo / walkthrough video:** https://drive.google.com/file/d/1ysq9PPy_SMdxTjWZA3CPprZTOJudyV-u/view?usp=sharing

End-to-end tests for the TheySaid app (`https://evo.dev.theysaid.io`), built with
**Playwright for Python** + **pytest**, using the Page Object Model and a recorded-
then-refactored workflow (record a flow with codegen, then turn it into a clean,
asserted Page Object test).

---

## Assignment scope

Implement automated e2e tests for four flows (registration is intentionally
skipped — it needs a manual OTP from email):

| # | Flow | Status |
|---|------|--------|
| 1 | **Log in** | ✅ Complete & passing |
| 2 | **Create a project** (AI Survey) | 🟡 **Half complete** — see note below |
| 3 | **Upload a document in Teach AI** | ✅ Complete & passing |
| 4 | **Publish a project + take its survey** | ❌ **Not completed** — see note below |

### Flow 2 is half-complete
The create-project test logs in, opens the **Add project** modal, selects the
**AI Survey** type, submits, and asserts that we land on the survey/form editor
(`/projects/new?project-type=Form&tab=form`). What it does **not** yet do is
configure and finalize the project content (adding questions, naming, saving) —
so the project is *initiated* but not *fully built out*. The remaining half is
the in-editor authoring steps.

### Flow 4 was not completed (time constraints)
The **publish a project + take its survey** flow was not implemented due to time
constraints. It spans two contexts — clicking Publish in the project editor, then
opening the public survey URL and submitting a response — and needs a dedicated
recording to capture the publish button and the survey-taking selectors reliably.
The structure here (page objects + `logged_in_page` fixture) is ready for it to
be dropped in as `pages/publish_page.py` + `tests/test_publish_and_survey.py`.

---

## Known bugs

Bugs found while building these tests. See [`bugs.txt`](bugs.txt) for full detail.

- **BUG-1 — Draft project creation hangs at 99%:** after selecting the draft
  project, it gets stuck at 99% on "Quality Assurance & Optimization" with no way
  to close it. *(High — blocks the flow.)*
- **BUG-2 — AI question generation ignores the selected type:** choosing a
  non-rating question type and then asking the AI to generate it always produces
  a ratings question.
- **BUG-3 — Publish button doesn't update after publishing:** the button still
  reads "Publish" after a project is published, making it look like the project
  may not be published yet.

`bugs.txt` also notes a testing trap: the project-type `data-test` ids don't match
their labels (e.g. *AI Survey* = `project-type-radio-form`).

---

## Project structure

```
tests/                      (repo root)
├── .env.example            # copy to .env and fill in credentials
├── .gitignore              # excludes .env, .auth/, caches
├── requirements.txt
├── pytest.ini              # default: chromium, headed, verbose
├── config.py               # loads .env -> Settings (base_url, email, password, sample_doc)
├── conftest.py             # fixtures: app_settings, auth_storage, logged_in_page
├── record.py               # launches `playwright codegen` to record new flows
├── bugs.txt                # bug log
├── NMR PART 2.docx         # sample document used by the Teach AI upload test
├── pages/                  # Page Object Model
│   ├── login_page.py
│   ├── create_project_page.py
│   └── teach_ai_page.py
└── tests/
    ├── test_login.py                # Flow 1
    ├── test_create_project.py       # Flow 2 (half complete)
    └── test_teach_ai_upload.py      # Flow 3
```

---

## Setup

Requires **Python 3.9+**.

```bash
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Install the Playwright browser (Chromium)
#    This repo expects browsers at D:\playwright-browsers (set in code via
#    PLAYWRIGHT_BROWSERS_PATH). If you don't have them there, either set that
#    env var to your browser cache, or run a normal install:
python -m playwright install chromium

# 3. Configure credentials
cp .env.example .env        # then edit .env with a real test account
```

`.env` (gitignored — never committed):

```
BASE_URL=https://evo.dev.theysaid.io
TEST_EMAIL=your-test-account@example.com
TEST_PASSWORD=your-password
```

---

## Running the tests

```bash
# All flows
python -m pytest

# A single flow
python -m pytest tests/test_login.py -v

# Headless (override the headed default in pytest.ini)
python -m pytest --headed=false
```

### How auth is reused
`test_login.py` exercises the full UI login. The other flows use the
`logged_in_page` fixture, which **logs in once per session**, caches the
authenticated storage state to `.auth/state.json`, and hands each test a
pre-authenticated page — so they don't repeat the login UI.

---

## Recording new flows

```bash
python record.py https://evo.dev.theysaid.io --output tests/test_new_flow.py
```

This opens Playwright's codegen recorder (browser on the left, generated code on
the right). Interact with the page; the generated Python is saved to the output
file. The recorded output is then refactored into a Page Object + asserted test
(that refactor is the manual step — codegen output is a starting point, not the
final test).

---

## Notes / design choices

- **Page Object Model** keeps selectors out of the tests; the non-obvious
  `data-test` mappings (see BUG note) live in `create_project_page.py`.
- **Selectors** prefer `data-test` attributes, falling back to role/text only
  where no `data-test` exists (e.g. the "Add file" button).
- **Browser binaries** are pinned to `D:\playwright-browsers` via
  `PLAYWRIGHT_BROWSERS_PATH` (set in `conftest.py` / `config.py` / `record.py`)
  to reuse a pre-installed cache and avoid re-downloading.
```
