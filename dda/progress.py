import sqlite3
import time
import os
from datetime import datetime

DB_PATH = "/Users/jackmcvickar/DiscoveryPortalMac/Data/dda.db"

def show_progress(start_time):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM files")
    total_files = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM extracts")
    total_extracts = cur.fetchone()[0]

    # Breakdown by source
    try:
        cur.execute("SELECT source, COUNT(*) FROM extracts GROUP BY source")
        breakdown = cur.fetchall()
    except sqlite3.OperationalError:
        breakdown = []

    conn.close()

    percent = (total_extracts / total_files * 100) if total_files else 0
    elapsed = time.time() - start_time
    avg_time = (elapsed / total_extracts) if total_extracts else 0

    os.system("clear")
    print("📊 Extraction Progress (auto-refresh)")
    print(f"   Files indexed:   {total_files}")
    print(f"   Files extracted: {total_extracts}")
    print(f"   Completion:      {percent:.2f}%")
    print(f"   Avg time/file:   {avg_time:.2f} sec")
    print(f"   Last refresh:    {datetime.now().strftime('%H:%M:%S')}")

    if breakdown:
        print("   Breakdown:")
        for source, count in breakdown:
            print(f"      {source}: {count}")

if __name__ == "__main__":
    start_time = time.time()
    try:
        while True:
            show_progress(start_time)
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n👋 Stopped monitoring.")
