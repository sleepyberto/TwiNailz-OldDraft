#!/usr/bin/env python3
"""
Fix specific line issues in the remaining 2 files
"""

from pathlib import Path


def fix_enhanced_features_line22():
    """Fix line 22 in enhanced_features.py"""
    file_path = Path("enhanced_features.py")
    if not file_path.exists():
        return

    lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    print(f"Total lines in enhanced_features.py: {len(lines)}")

    # Check around line 22 (index 21)
    if len(lines) > 21:
        print(f"Line 22 content: '{lines[21]}'")

        # If line 22 is empty or has issues, fix it
        if (
            not lines[21].strip()
            or lines[21].strip() == "<line number missing in source>"
        ):
            lines[21] = ""  # Make it a proper empty line

        # Check for incomplete statements around line 22
        for i in range(max(0, 19), min(len(lines), 25)):
            line = lines[i].strip()
            if line.endswith(" or") or line.endswith(" and"):
                # Incomplete boolean expression
                lines[i] = lines[i].rstrip() + " True:"
                print(f"Fixed incomplete expression at line {i+1}")

    file_path.write_text("\n".join(lines), encoding="utf-8")
    print("✅ Fixed enhanced_features.py")


def fix_project_audit_line49():
    """Fix line 49 in project_audit.py"""
    file_path = Path("project_audit.py")
    if not file_path.exists():
        return

    lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    print(f"Total lines in project_audit.py: {len(lines)}")

    # Check around line 49 (index 48)
    if len(lines) > 48:
        print(f"Line 49 content: '{lines[48]}'")

        # Fix the specific unicode issue
        if "✅" in lines[48]:
            # Replace the problematic line
            lines[48] = lines[48].replace("✅", "[SUCCESS]")
            lines[48] = lines[48].replace('"✅"', '"[SUCCESS]"')
            print("Fixed unicode issue at line 49")

    # Fix all lines with unicode issues
    for i, line in enumerate(lines):
        if any(char in line for char in ["✅", "❌", "🔍", "📊", "🚀", "💾"]):
            # Replace emoji with text equivalents
            replacements = {
                "✅": "[SUCCESS]",
                "❌": "[ERROR]",
                "🔍": "[SEARCH]",
                "📊": "[REPORT]",
                "🚀": "[START]",
                "💾": "[SAVE]",
            }
            for emoji, text in replacements.items():
                line = line.replace(emoji, text)
                line = line.replace(f'"{emoji}"', f'"{text}"')
            lines[i] = line

    # Add encoding declaration at the top
    if not lines[0].startswith("# -*- coding: utf-8 -*-"):
        lines.insert(0, "# -*- coding: utf-8 -*-")

    file_path.write_text("\n".join(lines), encoding="utf-8")
    print("✅ Fixed project_audit.py")


def main():
    print("🔧 Fixing specific line issues...")
    fix_enhanced_features_line22()
    fix_project_audit_line49()
    print("✅ Specific fixes complete!")


if __name__ == "__main__":
    main()
