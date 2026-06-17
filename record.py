"""
Launch Playwright's codegen (recording) mode.

Usage:
    python record.py                        # opens blank browser
    python record.py https://example.com    # opens at a specific URL
    python record.py https://example.com --output tests/test_login.py

The recorder watches your actions and generates pytest-playwright code.
When you close the inspector window the generated code is printed (or saved).
"""

import os
import subprocess
import sys

# Point Playwright at the local browser cache so no download is needed
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", r"D:\playwright-browsers")

def main() -> None:
    args = sys.argv[1:]

    url = ""
    output_file = ""

    i = 0
    positional = []
    while i < len(args):
        if args[i] in ("--output", "-o") and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        else:
            positional.append(args[i])
            i += 1

    if positional:
        url = positional[0]

    cmd = [
        sys.executable, "-m", "playwright", "codegen",
        "--browser", "chromium",
        "--viewport-size=1440,900",
    ]

    if output_file:
        cmd += ["--output", output_file]
        print(f"[record] Generated code will be saved to: {output_file}")

    if url:
        cmd.append(url)
        print(f"[record] Opening: {url}")
    else:
        print("[record] Opening blank browser — navigate to your target site.")

    print("[record] Close the Playwright Inspector window when you're done recording.\n")

    subprocess.run(cmd, env=os.environ)


if __name__ == "__main__":
    main()
