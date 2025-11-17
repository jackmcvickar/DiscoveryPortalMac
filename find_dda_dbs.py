#!/usr/bin/env python3
# =============================================================================
# File: find_dda_dbs.py
# Path: /Users/jackmcvickar/DiscoveryPortalMac/
# Purpose: Enforce canonical DB path and verify existence
# Version: 1.4.2
# Last Updated: 2025-11-13 14:10 CST
# =============================================================================

import os
import sqlite3

# Resolve canonical DB path relative to project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(PROJECT_ROOT, "Data", "dda.db")

def verify_db():
    """Check if canonical DB exists and is accessible."""
    if not os.path.isfile(DB_PATH):
        print(f"❌ Canonical DB not found at {DB_PATH}")
        return False

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()

        print(f"✅ Canonical DB found at {DB_PATH}")
        print("Tables present:")
        for t in tables:
            print(f" - {t[0]}")
        return True
    except Exception as e:
        print(f"⚠️ Error opening DB at {DB_PATH}: {e}")
        return False

def main():
    verify_db()

if __name__ == "__main__":
    main()

# end of script