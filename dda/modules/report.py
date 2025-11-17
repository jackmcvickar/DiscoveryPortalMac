#!/usr/bin/env python3
# =============================================================================
# File: report.py
# Purpose: Summarize document extraction status from dda.db, with folder breakdown
# =============================================================================

import os
import sqlite3

# Canonical database path
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "dda.db")

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Ensure schema exists (self-healing)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL,
            folder TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING'
        )
    """)
    conn.commit()

    # Global counts
    cur.execute("SELECT COUNT(*) FROM documents")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM documents WHERE status='PENDING'")
    pending = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM documents WHERE status='PROCESSED'")
    processed = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM documents WHERE status='FAILED'")
    failed = cur.fetchone()[0]

    print("===== Document Extraction Report =====")
    print(f"📊 Total files:     {total}")
    print(f"⏳ Pending:         {pending}")
    print(f"✅ Processed:       {processed}")
    print(f"❌ Failed:          {failed}")
    print("======================================")

    # Folder breakdown (all folders)
    print("\n===== Breakdown by Folder =====")
    cur.execute("""
        SELECT folder,
               COUNT(*) as total,
               SUM(CASE WHEN status='PENDING' THEN 1 ELSE 0 END) as pending,
               SUM(CASE WHEN status='PROCESSED' THEN 1 ELSE 0 END) as processed,
               SUM(CASE WHEN status='FAILED' THEN 1 ELSE 0 END) as failed
        FROM documents
        GROUP BY folder
        ORDER BY total DESC
    """)
    rows = cur.fetchall()
    for folder, total, pending, processed, failed in rows:
        folder_display = folder if folder else "(root)"
        print(f"📂 {folder_display}")
        print(f"   Total: {total}, Pending: {pending}, Processed: {processed}, Failed: {failed}")

    # Top 10 folders by file count with completion %
    print("\n===== Top 10 Folders by File Count =====")
    cur.execute("""
        SELECT folder,
               COUNT(*) as total,
               SUM(CASE WHEN status='PENDING' THEN 1 ELSE 0 END) as pending,
               SUM(CASE WHEN status='PROCESSED' THEN 1 ELSE 0 END) as processed,
               SUM(CASE WHEN status='FAILED' THEN 1 ELSE 0 END) as failed,
               ROUND(100.0 * SUM(CASE WHEN status='PROCESSED' THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_complete
        FROM documents
        GROUP BY folder
        ORDER BY total DESC
        LIMIT 10
    """)
    top_rows = cur.fetchall()
    for folder, total, pending, processed, failed, pct_complete in top_rows:
        folder_display = folder if folder else "(root)"
        print(f"📂 {folder_display}")
        print(f"   Total: {total}, Pending: {pending}, Processed: {processed}, Failed: {failed}, ✅ {pct_complete}% complete")

    conn.close()
    print("======================================")

if __name__ == "__main__":
    main()

# end of script