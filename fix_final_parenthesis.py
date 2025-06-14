#!/usr/bin/env python3
"""
Fix the final parenthesis issue in main_bot.py
"""

from pathlib import Path


def fix_main_bot_parenthesis():
    """Fix the stray ) at line 13"""
    file_path = Path("main_bot.py")
    lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    print(f"Checking line 13 in main_bot.py (total lines: {len(lines)})")

    if len(lines) > 12:  # Line 13 is index 12
        line_13 = lines[12]
        print(f"Line 13 content: '{line_13}'")

        # If line 13 is just a closing parenthesis
        if line_13.strip() == ")":
            # Remove this line or fix it
            lines.pop(12)  # Remove the problematic line
            print("Removed stray closing parenthesis")

        # Check for unbalanced parentheses around line 13
        for i in range(max(0, 10), min(len(lines), 16)):
            line = lines[i]
            open_parens = line.count("(")
            close_parens = line.count(")")

            if close_parens > open_parens:
                # Too many closing parens
                lines[i] = line.replace(")", "", close_parens - open_parens)
                print(f"Fixed line {i+1}: removed extra closing parentheses")

    file_path.write_text("\n".join(lines), encoding="utf-8")
    print("✅ Fixed main_bot.py")


def main():
    print("🔧 Fixing final parenthesis issue...")
    fix_main_bot_parenthesis()
    print("✅ Final fix complete!")


if __name__ == "__main__":
    main()
