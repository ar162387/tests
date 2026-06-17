"""Central test configuration — reads everything from environment / .env."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent

# Load .env that sits next to this file
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://evo.dev.theysaid.io")
    email: str = os.getenv("TEST_EMAIL", "")
    password: str = os.getenv("TEST_PASSWORD", "")
    # Sample document used by the Teach AI upload flow
    sample_doc: str = str(PROJECT_ROOT / "NMR PART 2.docx")


settings = Settings()
