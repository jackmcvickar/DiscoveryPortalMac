# backfill_hashes.py

import os
import sqlite3
import hashlib

DB_PATH = "/Users/jackmcvickar/DiscoveryPortalMac/Data/dda.db"

def file_hash(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, filepath FROM documents WHERE hash IS NULL OR hash = ''")
    rows = cursor.fetchall()

    for doc_id, filepath in rows:
        if os.path.exists(filepath):
            try:
                h = file_hash(filepath)
                cursor.execute("UPDATE documents SET hash=? WHERE id=?", (h, doc_id))
                print(f"Backfilled hash for {filepath}")
            except Exception as e:
                print(f"Error hashing {filepath}: {e}")
        else:
            print(f"File missing: {filepath}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

# end of script