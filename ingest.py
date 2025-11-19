import os
import sqlite3
import hashlib
import configparser

# Exclude junk/system files (PDFs are allowed now)
EXCLUDE_EXTENSIONS = {
    '.py', '.pyc', '.pyo', '.db', '.zip', '.csv',
    '.jpg', '.jpeg', '.png', '.gif', '.DS_Store'
}

def should_index(path):
    ext = os.path.splitext(path)[1].lower()
    return ext not in EXCLUDE_EXTENSIONS

def file_hash(path):
    """Generate a SHA256 hash for deduplication."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def upsert_document(conn, doc):
    sql = """
    INSERT INTO documents (category, filepath, filename, status, confidence,
                           last_modified, year, owner, account_id, period, hash)
    VALUES (:category, :filepath, :filename, :status, :confidence,
            :last_modified, :year, :owner, :account_id, :period, :hash)
    ON CONFLICT(hash) DO UPDATE SET
        category=excluded.category,
        filepath=excluded.filepath,
        filename=excluded.filename,
        status=excluded.status,
        confidence=excluded.confidence,
        last_modified=excluded.last_modified,
        year=excluded.year,
        owner=excluded.owner,
        account_id=excluded.account_id,
        period=excluded.period;
    """
    conn.execute(sql, doc)
    conn.commit()

def ingest_directory(conn, root_dir, category="Uncategorized"):
    print(f"Scanning {root_dir}...")
    processed = 0
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            if not should_index(fpath):
                print(f"Skipping {fpath}")
                continue

            print(f"Ingesting {fpath}")
            doc = {
                'category': category,
                'filepath': fpath,
                'filename': fname,
                'status': 'Inserted',
                'confidence': None,
                'last_modified': str(os.path.getmtime(fpath)),
                'year': None,
                'owner': None,
                'account_id': None,
                'period': None,
                'hash': file_hash(fpath)
            }
            upsert_document(conn, doc)
            processed += 1

    print(f"Ingestion complete. {processed} files ingested.")

if __name__ == "__main__":
    # Load config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Pull paths from [paths] section
    db_path = config.get("paths", "db_path")
    root_dir = config.get("paths", "docs_path")

    # Connect to DB
    conn = sqlite3.connect(db_path)

    # Ensure schema exists
    conn.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        filepath TEXT NOT NULL,
        filename TEXT NOT NULL,
        status TEXT NOT NULL,
        confidence REAL,
        last_modified TEXT NOT NULL,
        year TEXT,
        owner TEXT,
        account_id TEXT,
        period TEXT,
        hash TEXT NOT NULL UNIQUE
    );
    """)
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_documents_hash ON documents(hash);")

    # Run ingestion
    ingest_directory(conn, root_dir)

    conn.close()