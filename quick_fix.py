#!/usr/bin/env python3
"""
Quick syntax fixes for TwiNailz.AI
"""

import re
from pathlib import Path


def fix_syntax_errors():
    """Fix the 4 files that Black couldn't parse"""

    # Fix main_bot.py
    main_bot = Path("main_bot.py")
    if main_bot.exists():
        content = main_bot.read_text(encoding="utf-8-sig", errors="ignore")
        content = re.sub(r"<UPDATED_CODE>", "", content)
        main_bot.write_text(content, encoding="utf-8")
        print("✅ Fixed main_bot.py")

    # Fix enhanced_features.py
    enhanced = Path("enhanced_features.py")
    if enhanced.exists():
        lines = enhanced.read_text(encoding="utf-8-sig", errors="ignore").splitlines()
        for i, line in enumerate(lines):
            if "if 'brittle' in nail_concern or" in line and not line.strip().endswith(
                ":"
            ):
                lines[i] = line.rstrip() + " 'weak' in nail_concern:"
                break
        enhanced.write_text("\n".join(lines), encoding="utf-8")
        print("✅ Fixed enhanced_features.py")

    # Fix backup enhanced_features.py or remove it
    backup_enhanced = Path("backup_/enhanced_features.py")
    if backup_enhanced.exists():
        backup_enhanced.unlink()  # Delete duplicate
        print("🗑️ Removed backup duplicate")

    # Fix project_audit.py encoding
    audit = Path("project_audit.py")
    if audit.exists():
        try:
            content = audit.read_text(encoding="utf-8-sig", errors="replace")
            if not content.startswith("# -*- coding: utf-8 -*-"):
                content = "# -*- coding: utf-8 -*-\n" + content
            audit.write_text(content, encoding="utf-8")
            print("✅ Fixed project_audit.py")
        except Exception as e:
            print(f"⚠️ project_audit.py needs manual review: {e}")


if __name__ == "__main__":
    print("🔧 Fixing syntax errors...")
    fix_syntax_errors()
    print("\n✅ Ready to format with Black!")
