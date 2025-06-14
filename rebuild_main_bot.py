#!/usr/bin/env python3
"""
Completely rebuild main_bot.py with clean syntax
"""

from pathlib import Path


def rebuild_main_bot():
    """Rebuild main_bot.py from scratch with clean content"""
    file_path = Path("main_bot.py")

    # Read current content
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except:
        content = file_path.read_text(encoding="latin-1", errors="ignore")

    print(f"Original file size: {len(content)} characters")

    # Clean the content by removing any problematic characters
    # Keep only printable ASCII and common Unicode
    clean_content = ""
    for char in content:
        if ord(char) < 127 or char in ["\n", "\r", "\t"]:
            clean_content += char
        elif char.isprintable():
            clean_content += char

    print(f"Cleaned file size: {len(clean_content)} characters")

    # Split into lines and rebuild properly
    lines = clean_content.splitlines()

    # Create the new file structure
    new_lines = [
        "#!/usr/bin/env python3",
        "# -*- coding: utf-8 -*-",
        '"""',
        "TwiNailz.AI - Advanced Nail Care AI Bot",
        "Main bot functionality",
        '"""',
        "",
        "import asyncio",
        "import logging",
        "import os",
        "import sys",
        "from datetime import datetime",
        "from pathlib import Path",
        "",
        "try:",
        "    from config import BOT_TOKEN",
        "except ImportError:",
        '    BOT_TOKEN = os.getenv("BOT_TOKEN", "your-token-here")',
        "",
        "# Configure logging",
        "logging.basicConfig(",
        "    level=logging.INFO,",
        '    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"',
        ")",
        "logger = logging.getLogger(__name__)",
        "",
    ]

    # Find and preserve the main bot logic
    in_function = False

    for line in lines:
        stripped = line.strip()

        # Skip the problematic header section
        if any(
            skip in stripped
            for skip in [
                "from config import",
                "import config",
                "#!/usr/bin",
                "# -*- coding",
                "TwiNailz.AI",
                "Main bot",
                "Advanced Nail",
            ]
        ):
            continue

        # Keep function definitions and class definitions
        if stripped.startswith(("def ", "class ", "async def ")):
            new_lines.append("")
            new_lines.append(line)
            in_function = True
            len(line) - len(line.lstrip())
        elif in_function and line.strip():
            new_lines.append(line)
        elif in_function and not line.strip():
            new_lines.append("")
        elif stripped.startswith(("if __name__", "if __name__ ==")):
            new_lines.append("")
            new_lines.append(line)
            in_function = True
        elif stripped and not in_function:
            # Global code outside functions
            if not any(skip in stripped for skip in ["import ", "from "]):
                new_lines.append(line)

    # Add a simple main section if none exists
    if not any("if __name__" in line for line in new_lines):
        new_lines.extend(
            [
                "",
                "def main():",
                '    """Main function"""',
                '    logger.info("TwiNailz.AI Bot starting...")',
                "    # Add your bot logic here",
                "    pass",
                "",
                'if __name__ == "__main__":',
                "    main()",
            ]
        )

    # Write the clean file
    file_path.write_text("\n".join(new_lines), encoding="utf-8")
    print(f"✅ Rebuilt main_bot.py with {len(new_lines)} lines")


def main():
    print("🔥 Rebuilding main_bot.py from scratch...")
    rebuild_main_bot()
    print("✅ Rebuild complete!")


if __name__ == "__main__":
    main()
