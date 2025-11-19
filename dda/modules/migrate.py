#!/usr/bin/env python3
# =============================================================================
# File: migrate.py
# Purpose: Schema migration and cleanup for dda.db, driven by config.ini
# =============================================================================

import sqlite3
import os
import configparser

# Paths
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "Data", "dda.db")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config.ini")

def column_exists(conn, table, column):
    cursor = conn.execute(f"PRAGMA table_info({table});")
    return any(row[1] == column for row in cursor.fetchall())

def load_exclusions():
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH)
    folders = [f.strip() for f in parser.get("exclusions", "folders", fallback="").split(",") if f.strip()]
    extensions = [e.strip().lower() for e in parser.get("exclusions", "extensions", fallback="").split(",") if e.strip()]
    return folders, extensions

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Ensure tags column exists
    if not column_exists(conn, "documents", "tags"):
        print("🛠 Adding 'tags' column to documents table...")
        cursor.execute("ALTER TABLE documents ADD COLUMN tags TEXT;")
        conn.commit()
    else:
        print("✅ 'tags' column already exists.")

    # 2. Ensure text_source column exists
    if not column_exists(conn, "documents", "text_source"):
        print("🛠 Adding 'text_source' column to documents table...")
        cursor.execute("ALTER TABLE documents ADD COLUMN text_source TEXT;")
        conn.commit()
    else:
        print("✅ 'text_source' column already exists.")

    # 3. Load exclusions from config.ini
    exclude_folders, exclude_exts = load_exclusions()
    print(f"🚫 Excluding folders from config.ini: {exclude_folders}")
    print(f"🚫 Excluding extensions from config.ini: {exclude_exts}")

    # 4. Remove junk categories
    for cat in exclude_folders:
        print(f"🚫 Removing category '{cat}'...")
        cursor.execute("DELETE FROM documents WHERE category = ?;", (cat,))
    conn.commit()

    # 5. Show summary
    cursor.execute("SELECT category, COUNT(*) FROM documents GROUP BY category ORDER BY COUNT(*) DESC LIMIT 10;")
    rows = cursor.fetchall()
    print("\n📊 Top categories after cleanup:")
    for category, count in rows:
        print(f"  {category}: {count} files")

    conn.close()
    print("✅ Migration complete.")

if __name__ == "__main__":
    migrate()
# end of script