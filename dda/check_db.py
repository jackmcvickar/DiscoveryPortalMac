import sqlite3

DB_PATH = "/Users/jackmcvickar/DiscoveryPortalMac/Data/dda.db"

def check_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # List all tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    print("📋 Tables:", tables)

    # Count rows in key tables
    for table in ["files", "extracts", "accounts", "documents", "statements", "transactions", "gaps"]:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"   {table}: {count} rows")
        except Exception as e:
            print(f"   {table}: not found ({e})")

    conn.close()

if __name__ == "__main__":
    check_db()
