#!/usr/bin/env python3
"""
Final fixes for the last 2 problematic files
"""

import re
from pathlib import Path


def fix_project_audit_final():
    """Fix remaining [SUCCESS] issues in project_audit.py"""
    file_path = Path("project_audit.py")
    lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    print(f"Checking {len(lines)} lines in project_audit.py")

    # Fix all lines that have the pattern: "[SUCCESS]" followed by text
    for i, line in enumerate(lines):
        if '"[SUCCESS]"' in line and not line.strip().startswith("#"):
            # Convert to comment
            lines[i] = "    # " + line.strip().replace('"[SUCCESS]"', "[SUCCESS]")
            print(f"Fixed line {i+1}: {lines[i]}")
        elif (
            "[SUCCESS]" in line
            and not line.strip().startswith("#")
            and not "print" in line
        ):
            # Make sure it's a comment
            lines[i] = "    # " + line.strip()
            print(f"Fixed line {i+1}: {lines[i]}")

    file_path.write_text("\n".join(lines), encoding="utf-8")
    print("✅ Fixed project_audit.py")


def fix_main_bot_final():
    """Fix markdown text in main_bot.py"""
    file_path = Path("main_bot.py")
    lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    print(f"Checking {len(lines)} lines in main_bot.py")

    # Fix line 278 and similar markdown-style lines
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("**") and stripped.endswith(":**"):
            # Convert markdown to Python comment
            lines[i] = "    # " + stripped.replace("**", "").replace(":", "")
            print(f"Fixed line {i+1}: {lines[i]}")
        elif stripped.startswith("**") and "**" in stripped:
            # Other markdown formatting
            lines[i] = "    # " + re.sub(r"\*\*(.*?)\*\*", r"\1", stripped)
            print(f"Fixed line {i+1}: {lines[i]}")
        elif (
            stripped
            and not stripped.startswith(("#", '"', "'"))
            and not any(
                char in stripped
                for char in [
                    "=",
                    "(",
                    ")",
                    "[",
                    "]",
                    "def ",
                    "class ",
                    "import ",
                    "from ",
                ]
            )
        ):
            # Looks like plain text that should be a comment
            if len(stripped) > 5 and not stripped.isdigit():
                lines[i] = "    # " + stripped
                print(f"Fixed potential comment line {i+1}: {lines[i]}")

    file_path.write_text("\n".join(lines), encoding="utf-8")
    print("✅ Fixed main_bot.py")


def main():
    print("🎯 Final fixes for the last 2 files...")
    fix_project_audit_final()
    fix_main_bot_final()
    print("✅ All final fixes applied!")


if __name__ == "__main__":
    main()
