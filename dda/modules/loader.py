#!/usr/bin/env python3
# =============================================================================
# File: loader.py
# Purpose: Load document file paths into ./Data/dda.db with progress counters
# =============================================================================

import sqlite3
import os
import configparser
from tabulate import tabulate

# ---------------------------------------------------------------------------
# Load config.ini
# ---------------------------------------------------------------------------
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "..", "config.ini"))

DB_PATH = config.get("paths", "db_path", fallback="./Data/dda.db")
DOCS_PATH = config.get("paths", "docs_path", fallback="./Docs")

def connect_db():
    return sqlite3.connect(DB_PATH)

def count_files():
    """Count total files under DOCS_PATH (excluding hidden)."""
    total = 0
    for root, _, files in os.walk(DOCS_PATH):
        for fname in files:
            if not fname.startswith("."):
                total += 1
    return total

def load_documents():
    conn = connect_db()
    cur = conn.cursor()

    total_files = count_files()
    loaded = 0
    skipped = 0

    for root, _, files in os.walk(DOCS_PATH):
        for fname in files:
            if fname.startswith("."):
                continue

            filepath = os.path.join(root, fname)
            if not os.path.isfile(filepath):
                continue

            try:
                # Check if file already exists in DB with non-pending status
                cur.execute("SELECT status FROM documents WHERE filepath = ?", (filepath,))
                row = cur.fetchone()
                if row and row[0] in ("complete", "error"):
                    skipped += 1
                    print(f"⏭️ Skipped {filepath} (already {row[0]})")
                    continue

                # Insert or update as pending
                cur.execute(
                    "INSERT OR IGNORE INTO documents (filepath, status) VALUES (?, 'pending')",
                    (filepath,),
                )
                loaded += 1
                pct = (loaded / total_files) * 100 if total_files else 0
                print(f"[{loaded}/{total_files} | {pct:.1f}%] Loaded {filepath}")

            except Exception as e:
                print(f"⚠️ Could not insert {filepath}: {e}")

    conn.commit()

    # Summary counts
    cur.execute("SELECT COUNT(*) FROM documents WHERE status='pending'")
    pending = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM documents WHERE status='complete'")
    complete = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM documents WHERE status='error'")
    error = cur.fetchone()[0]

    conn.close()

    print("\n📊 Loader Summary")
    table = [
        ["Total scanned", total_files],
        ["Inserted (pending)", loaded],
        ["Skipped (already complete/error)", skipped],
        ["Pending in DB", pending],
        ["Complete in DB", complete],
        ["Error in DB", error],
    ]
    print(tabulate(table, headers=["Status", "Count"], tablefmt="grid"))

    print(f"\n✅ Data loading complete. {loaded}/{total_files} files inserted, {skipped} skipped.")

if __name__ == "__main__":
    load_documents()

# end of script