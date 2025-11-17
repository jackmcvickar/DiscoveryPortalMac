#!/usr/bin/env python3
# =============================================================================
# File: check_db_path.py
# Purpose: Scan project scripts for DB path references and enforce ./Data/dda.db
# =============================================================================

import os
import sys

ROOT_DIR = "."
CANONICAL = "./Data/dda.db"
BAD_PATHS = ["./Data/dda.db", "./Data/dda.db"]

def scan_file(filepath):
    issues = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f, start=1):
                for bad in BAD_PATHS:
                    if bad in line:
                        issues.append((i, line.strip(), bad))
    except Exception as e:
        print(f"⚠️ Could not read {filepath}: {e}")
    return issues

def fix_file(filepath):
    """Rewrite bad paths to canonical path."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        for bad in BAD_PATHS:
            content = content.replace(bad, CANONICAL)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"🛠️ Fixed {filepath}")
    except Exception as e:
        print(f"⚠️ Could not fix {filepath}: {e}")

def main():
    fix_mode = "--fix" in sys.argv
    print("🔍 Scanning for DB path references...\n")
    flagged = {}
    for root, _, files in os.walk(ROOT_DIR):
        for fname in files:
            if fname.endswith((".py", ".sh")):
                fpath = os.path.join(root, fname)
                issues = scan_file(fpath)
                if issues:
                    flagged[fpath] = issues
                    if fix_mode:
                        fix_file(fpath)

    if not flagged:
        print("✅ All scripts reference canonical DB path only:", CANONICAL)
    else:
        if not fix_mode:
            print("❌ Found non-canonical DB references:\n")
            for fpath, issues in flagged.items():
                print(f"File: {fpath}")
                for (line_no, line, bad) in issues:
                    print(f"  Line {line_no}: {line}  (bad path: {bad})")
                print()
        else:
            print("\n✅ Auto-fix complete. All bad paths replaced with:", CANONICAL)

if __name__ == "__main__":
    main()

# end of script