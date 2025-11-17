import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("/Users/jackmcvickar/DiscoveryPortalMac/data/dda.db")

def print_status_summary():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT status, COUNT(*) FROM documents GROUP BY status;")
    rows = cur.fetchall()
    conn.close()
    print("📊 Status Summary:")
    for status, count in rows:
        label = status if status is not None else "NULL"
        print(f"   {label}: {count}")
    return rows

def log_status_summary(rows):
    today = datetime.now().strftime("%Y%m%d")
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"status_summary_{today}.log"
    with open(log_file, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n[{timestamp}] Status Summary:\n")
        for status, count in rows:
            label = status if status is not None else "NULL"
            f.write(f"   {label}: {count}\n")

def export_final_summary():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT status, COUNT(*) FROM documents GROUP BY status;")
    rows = cur.fetchall()
    conn.close()

    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    final_path = report_dir / "final_status_summary.csv"
    with open(final_path, "w") as f:
        f.write("status,count\n")
        for status, count in rows:
            label = status if status is not None else "NULL"
            f.write(f"{label},{count}\n")
    print(f"📑 Final status summary exported to {final_path}")
# end of script