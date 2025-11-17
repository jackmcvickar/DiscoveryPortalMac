import sqlite3

def list_tables(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("Tables in database:")
    for table in tables:
        print(f"- {table[0]}")
    conn.close()

if __name__ == '__main__':
    db_path = '/Users/jackmcvickar/DiscoveryPortalMac/data/dda.db'  # Update if needed
    list_tables(db_path)
