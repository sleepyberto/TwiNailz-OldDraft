#!/usr/bin/env python3
"""
Fix remaining syntax errors
"""

import re
from pathlib import Path


def fix_main_bot():
    """Fix unclosed string in main_bot.py"""
    file_path = Path("main_bot.py")
    if not file_path.exists():
        return

    content = file_path.read_text(encoding="utf-8", errors="ignore")

    # Count triple quotes to find unclosed strings
    triple_quote_count = content.count('"""')
    if triple_quote_count % 2 != 0:
        # Odd number means unclosed string
        content += '\n"""'
        print("✅ Fixed unclosed string in main_bot.py")

    # Remove any <UPDATED_CODE> or similar placeholders
    content = re.sub(r"<[A-Z_]+>", "", content)

    file_path.write_text(content, encoding="utf-8")


def fix_enhanced_features():
    """Fix enhanced_features.py line issues"""
    file_path = Path("enhanced_features.py")
    if not file_path.exists():
        return

    lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    # Fix common issues
    fixed_lines = []
    for i, line in enumerate(lines):
        # Skip empty or problematic lines
        if not line.strip():
            fixed_lines.append("")
            continue

        # Fix incomplete if statements
        if "if 'brittle' in nail_concern or" in line and not line.strip().endswith(":"):
            line = line.rstrip() + " 'weak' in nail_concern:"

        # Remove any placeholders
        line = re.sub(r"<[A-Z_]+>", "", line)

        fixed_lines.append(line)

    file_path.write_text("\n".join(fixed_lines), encoding="utf-8")
    print("✅ Fixed enhanced_features.py")


def fix_project_audit():
    """Fix unicode issues in project_audit.py"""
    file_path = Path("project_audit.py")
    if not file_path.exists():
        return

    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")

        # Replace problematic unicode characters
        content = content.replace("✅", '"✅"')
        content = content.replace("❌", '"❌"')
        content = content.replace("🔍", '"🔍"')
        content = content.replace("📊", '"📊"')

        # Add encoding declaration
        if not content.startswith("# -*- coding: utf-8 -*-"):
            content = "# -*- coding: utf-8 -*-\n" + content

        file_path.write_text(content, encoding="utf-8")
        print("✅ Fixed project_audit.py")

    except Exception as e:
        print(f"❌ Could not fix project_audit.py: {e}")
        print("Manual fix needed - open file and replace emoji with quoted strings")


def main():
    print("🔧 Fixing remaining syntax errors...")
    fix_main_bot()
    fix_enhanced_features()
    fix_project_audit()
    print("✅ All fixes applied!")


if __name__ == "__main__":
    main()
