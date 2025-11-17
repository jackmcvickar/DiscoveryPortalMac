#!/usr/bin/env python3
# =============================================================================
# File: migrate_documents.py
# Purpose: Ensure documents table has filepath, status, extracted_text columns
# =============================================================================

import sqlite3

DB_PATH = "./Data/dda.db"

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create table if missing
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filepath TEXT UNIQUE,
            status TEXT DEFAULT 'pending',
            extracted_text TEXT
        )
    """)

    # Check schema
    cur.execute("PRAGMA table_info(documents);")
    cols = [row[1] for row in cur.fetchall()]
    print("📊 Current columns:", cols)

    # If filepath missing, rebuild table
    if "filepath" not in cols:
        print("⚠️ filepath column missing, rebuilding table...")
        cur.execute("ALTER TABLE documents RENAME TO documents_old;")
        cur.execute("""
            CREATE TABLE documents (
                id INTEGER PRIMARY KEY,
                filepath TEXT UNIQUE,
                status TEXT DEFAULT 'pending',
                extracted_text TEXT
            )
        """)
        # Copy over any old data if possible
        try:
            cur.execute("INSERT INTO documents (id, status) SELECT id, status FROM documents_old;")
            print("✅ Migrated old data into new schema")
        except Exception as e:
            print("⚠️ Could not migrate old data:", e)
        cur.execute("DROP TABLE documents_old;")

    conn.commit()
    conn.close()
    print("✅ Migration complete. Schema is ready.")

if __name__ == "__main__":
    migrate()

# end of script