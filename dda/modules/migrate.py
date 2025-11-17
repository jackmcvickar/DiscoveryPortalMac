import sqlite3
from pathlib import Path

DB_PATH = Path("/Users/jackmcvickar/DiscoveryPortalMac/data/dda.db")

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ✅ Ensure documents table exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            account_id TEXT,
            owner TEXT,
            period TEXT,
            confidence REAL,
            filepath TEXT,
            filesize INTEGER,
            hash TEXT,
            last_modified TEXT,
            account_number_last4 TEXT,
            year TEXT,
            status TEXT,
            filename TEXT
        );
    """)

    # ✅ Check existing columns
    cur.execute("PRAGMA table_info(documents);")
    cols = [row[1] for row in cur.fetchall()]

    if "filename" not in cols:
        print("🔧 Adding missing 'filename' column...")
        cur.execute("ALTER TABLE documents ADD COLUMN filename TEXT;")

    if "status" not in cols:
        print("🔧 Adding missing 'status' column with default...")
        cur.execute("ALTER TABLE documents ADD COLUMN status TEXT DEFAULT 'unprocessed';")

    # ✅ Create indexes safely
    cur.execute("CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_documents_filepath ON documents(filepath);")

    # ✅ One-time cleanup: set NULL statuses to 'unprocessed'
    cur.execute("UPDATE documents SET status='unprocessed' WHERE status IS NULL;")

    conn.commit()
    conn.close()
    print("✅ Migration complete (NULL statuses normalized)")

if __name__ == "__main__":
    migrate()
# end of script