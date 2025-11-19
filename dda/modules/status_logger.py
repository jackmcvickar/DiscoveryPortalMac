#!/usr/bin/env python3
import sqlite3, os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "Data", "dda.db")

def print_status_summary(conn=None):
    """Print category counts. If no conn, open DB_PATH."""
    if conn is None:
        conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT category, COUNT(*) FROM documents GROUP BY category").fetchall()
    print("📊 Category summary:")
    for cat, count in rows:
        print(f"  {cat}: {count} files")

def log_status_summary(conn, logfile="status.log"):
    """Log DB summary to file."""
    rows = conn.execute("SELECT category, COUNT(*) FROM documents GROUP BY category").fetchall()
    with open(logfile, "a") as f:
        f.write(f"\n=== Status Summary {datetime.now().isoformat()} ===\n")
        for cat, count in rows:
            f.write(f"{cat}: {count} files\n")

def export_final_summary(conn, outfile="final_summary.txt"):
    """Export text_source coverage."""
    rows = conn.execute("SELECT text_source, COUNT(*) FROM documents GROUP BY text_source").fetchall()
    with open(outfile, "w") as f:
        f.write(f"=== Final Summary {datetime.now().isoformat()} ===\n")
        for src, count in rows:
            f.write(f"{src or 'None'}: {count} docs\n")

def log_status_message(msg, logfile="status.log"):
    """Log a plain string message (not DB summary)."""
    with open(logfile, "a") as f:
        f.write(f"{datetime.now().isoformat()} - {msg}\n")

def log_status(conn_or_msg, logfile="status.log"):
    """Compatibility wrapper: if string, log message; if conn, log summary."""
    if isinstance(conn_or_msg, str):
        return log_status_message(conn_or_msg, logfile=logfile)
    return log_status_summary(conn_or_msg, logfile=logfile)

# end of script