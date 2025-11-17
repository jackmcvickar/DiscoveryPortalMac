import sqlite3

def print_documents_schema(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(documents);")
    columns = cur.fetchall()
    print("Documents table schema:")
    for col in columns:
        print(f"- {col[1]} (type: {col[2]})")
    conn.close()


if __name__ == '__main__':
    db_path = '/Users/jackmcvickar/DiscoveryPortalMac/data/dda.db'
    print_documents_schema(db_path)

# End of script
