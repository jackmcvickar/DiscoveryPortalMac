#!/usr/bin/env python3
# =============================================================================
# File: setup_schema.py
# Purpose: Ensure canonical schema exists in ./Data/dda.db
# =============================================================================

import sqlite3
import os

DB_PATH = "./Data/dda.db"

def setup():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create documents table if missing
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filepath TEXT UNIQUE,
            status TEXT DEFAULT 'pending',
            extracted_text TEXT
        )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Schema ensured in {DB_PATH}")

if __name__ == "__main__":
    setup()

# end of script