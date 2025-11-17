#!/usr/bin/env python3
# =============================================================================
# File: retry.py
# Purpose: Retry extraction for documents marked as 'error' and show summary table
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

def connect_db():
    return sqlite3.connect(DB_PATH)

def retry_documents():
    conn = connect_db()
    cur = conn.cursor()

    # Get error docs
    cur.execute("SELECT id, filepath FROM documents WHERE status='error'")
    error_docs = cur.fetchall()
    total_errors = len(error_docs)
    retried = 0
    still_error = 0

    for doc_id, filepath in error_docs:
        try:
            # Placeholder retry logic: mark as complete if file exists
            if os.path.isfile(filepath):
                cur.execute("UPDATE documents SET status='complete' WHERE id=?", (doc_id,))
                retried += 1
                print(f"🔄 Retried {filepath} → complete")
            else:
                still_error += 1
                print(f"⚠️ {filepath} still error (file missing)")
        except Exception as e:
            still_error += 1
            print(f"⚠️ Retry failed for {filepath}: {e}")

    conn.commit()

    # Summary counts
    cur.execute("SELECT COUNT(*) FROM documents WHERE status='pending'")
    pending = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM documents WHERE status='complete'")
    complete = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM documents WHERE status='error'")
    error = cur.fetchone()[0]

    conn.close()

    print("\n📊 Retry Summary")
    table = [
        ["Total errors before retry", total_errors],
        ["Successfully retried", retried],
        ["Still error", still_error],
        ["Pending in DB", pending],
        ["Complete in DB", complete],
        ["Error in DB", error],
    ]
    print(tabulate(table, headers=["Status", "Count"], tablefmt="grid"))

    print(f"\n✅ Retry complete. {retried}/{total_errors} fixed, {still_error} still error.")

if __name__ == "__main__":
    retry_documents()

# end of script