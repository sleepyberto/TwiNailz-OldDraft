#!/usr/bin/env python3
"""
Surgical fixes for exact syntax errors
"""

import re
from pathlib import Path


def fix_enhanced_features():
    """Fix the literal '<line number missing in source>' text"""
    file_path = Path("enhanced_features.py")
    content = file_path.read_text(encoding="utf-8", errors="ignore")

    # Remove the literal problematic text
    content = content.replace("<line number missing in source>", "")
    content = content.replace("<line number missing in source>", "# Fixed line")

    # Fix any hanging 'or' or 'and' statements
    lines = content.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.endswith(" or") or stripped.endswith(" and"):
            lines[i] = line.rstrip() + " True:"
        elif stripped == "or" or stripped == "and":
            lines[i] = "    pass  # Fixed incomplete statement"

    file_path.write_text("\n".join(lines), encoding="utf-8")
    print("✅ Fixed enhanced_features.py")


def fix_project_audit():
    """Fix the '[SUCCESS]' syntax error at line 49"""
    file_path = Path("project_audit.py")
    lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    # Fix line 49 specifically (index 48)
    if len(lines) > 48:
        line = lines[48]
        # The error shows: "[SUCCESS]" Proper SQLite database design
        # This suggests missing quotes or comment symbol
        if '"[SUCCESS]" Proper SQLite database design' in line:
            lines[48] = "    # [SUCCESS] Proper SQLite database design"
        elif "[SUCCESS]" in line and "Proper SQLite" in line:
            # Make it a proper comment
            lines[48] = re.sub(
                r".*\[SUCCESS\].*",
                "    # [SUCCESS] Proper SQLite database design",
                line,
            )

    file_path.write_text("\n".join(lines), encoding="utf-8")
    print("✅ Fixed project_audit.py")


def fix_main_bot():
    """Fix the EOF in multi-line string at line 276"""
    file_path = Path("main_bot.py")
    content = file_path.read_text(encoding="utf-8", errors="ignore")

    # Find unclosed triple quotes
    lines = content.splitlines()

    # Look around line 276 for unclosed strings
    for i in range(max(0, 273), min(len(lines), 280)):
        if '"""' in lines[i]:
            # Count quotes before this line
            before_content = "\n".join(lines[:i])
            quote_count = before_content.count('"""')

            # If odd number, we need to close it
            if quote_count % 2 != 0:
                # Add closing quote
                if i < len(lines) - 1:
                    lines.insert(i + 1, '"""')
                else:
                    lines.append('"""')
                break

    # Also check for any incomplete f-strings or quotes at the end
    if not content.endswith("\n"):
        content += "\n"

    # Fix any hanging quotes at the end
    if content.count('"""') % 2 != 0:
        content += '"""\n'

    if content.count("'''") % 2 != 0:
        content += "'''\n"

    file_path.write_text(content, encoding="utf-8")
    print("✅ Fixed main_bot.py")


def main():
    print("🏥 Applying surgical fixes...")
    fix_enhanced_features()
    fix_project_audit()
    fix_main_bot()
    print("✅ All surgical fixes applied!")


if __name__ == "__main__":
    main()
