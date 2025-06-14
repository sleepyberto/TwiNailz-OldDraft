#!/usr/bin/env python3
"""
Emergency fix for main_bot.py header
"""

from pathlib import Path


def fix_main_bot_header():
    """Fix the problematic header section of main_bot.py"""
    file_path = Path("main_bot.py")
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    print("Current first 15 lines:")
    for i in range(min(15, len(lines))):
        print(f"{i+1:2d}: {repr(lines[i])}")

    # Find where the real Python code starts
    python_start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith(
            ("import ", "from ", "#!/usr/bin/env", "# -*- coding:", "def ", "class ")
        ):
            python_start = i
            break

    # Create clean header
    clean_header = [
        "#!/usr/bin/env python3",
        "# -*- coding: utf-8 -*-",
        '"""',
        "TwiNailz.AI - Advanced Nail Care AI Bot",
        '"""',
        "",
        "import asyncio",
        "import logging",
        "import os",
        "from datetime import datetime",
        "from pathlib import Path",
        "",
        "from config import BOT_TOKEN",
        "",
    ]

    # Keep everything after the problematic header
    remaining_lines = lines[python_start + 1 :] if python_start < len(lines) else []

    # Combine clean header with remaining content
    new_content = clean_header + remaining_lines

    file_path.write_text("\n".join(new_content), encoding="utf-8")
    print("✅ Created clean header for main_bot.py")


def main():
    print("🚨 Emergency fix for main_bot.py header...")
    fix_main_bot_header()
    print("✅ Emergency fix complete!")


if __name__ == "__main__":
    main()
