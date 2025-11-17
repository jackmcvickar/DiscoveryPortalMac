import os
import hashlib
import sqlite3
import json
from datetime import datetime

DB_PATH = "/Users/jackmcvickar/DiscoveryPortalMac/Data/dda.db"
DATA_DIR = "/Users/jackmcvickar/DiscoveryPortalMac/Data"

def sha256_file(path):
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def index_files():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for root, _, files in os.walk(DATA_DIR):
        for fname in files:
            fpath = os.path.join(root, fname)

            # Skip the database itself
            if fpath.endswith("dda.db"):
                continue

            try:
                size = os.path.getsize(fpath)
                mtime = datetime.fromtimestamp(os.path.getmtime(fpath)).isoformat()
                sha256 = sha256_file(fpath)

                # Break down folder hierarchy relative to DATA_DIR
                rel_path = os.path.relpath(root, DATA_DIR)
                folder_parts = rel_path.split(os.sep) if rel_path != "." else []
                folder_json = json.dumps(folder_parts)

                cur.execute("""
                    INSERT INTO files (path, folder_path, sha256, size_bytes, modified_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (fpath, folder_json, sha256, size, mtime))

                print(f"Indexed: {fpath} (folders={folder_parts})")
            except Exception as e:
                print(f"⚠️ Skipped {fpath}: {e}")

    conn.commit()
    conn.close()
    print("✅ Indexing complete.")

if __name__ == "__main__":
    index_files()
