#!/usr/bin/env python3
# =============================================================================
# File: dashboard.py
# Purpose: Display progress summary of document extraction
# =============================================================================

import sqlite3
from tabulate import tabulate

DB_PATH = "./Data/dda.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def get_status_counts():
    """Return counts of documents by status."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT status, COUNT(*) FROM documents GROUP BY status")
    rows = cur.fetchall()
    conn.close()
    return dict(rows)

def show_dashboard():
    """Print a summary dashboard of document statuses."""
    counts = get_status_counts()
    total = sum(counts.values())

    table = [
        ["Pending", counts.get("pending", 0)],
        ["In Progress", counts.get("in_progress", 0)],
        ["Complete", counts.get("complete", 0)],
        ["Error", counts.get("error", 0)],
        ["Total", total],
    ]

    print("\n📊 Divorce Discovery Assistant Dashboard\n")
    print(tabulate(table, headers=["Status", "Count"], tablefmt="fancy_grid"))

    if total > 0:
        pct_complete = (counts.get("complete", 0) / total) * 100
        print(f"\nProgress: {pct_complete:.2f}% complete\n")

if __name__ == "__main__":
    show_dashboard()

# end of script