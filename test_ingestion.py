# test_ingestion.py

import os
import sqlite3
import datetime

def load_flat_ini(path="config.ini"):
    values = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            values[key.strip()] = val.strip()
    return values

config = load_flat_ini("config.ini")

DB_PATH = config["db_path"]
SOURCE_DIR = config["docs_path"]

def insert_document(db_conn, file_path: str, category: str = "Uncategorized", status: str = "New"):
    filename = os.path.basename(file_path)
    processed_at = datetime.datetime.now().isoformat()

    cursor = db_conn.cursor()
    cursor.execute(
        """
        INSERT INTO documents (
            category, filepath, filename, status, confidence, last_modified, year
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            category,
            file_path,
            filename,
            status,
            0.95,
            processed_at,
            str(datetime.datetime.now().year),
        ),
    )
    db_conn.commit()

def main():
    print("=== Sanity Check ===")
    print(f"DB_PATH: {DB_PATH}")
    print(f"SOURCE_DIR: {SOURCE_DIR}")
    print("====================")

    conn = sqlite3.connect(DB_PATH)

    for root, _, files in os.walk(SOURCE_DIR):
        for f in files:
            if f.lower().endswith((".pdf", ".jpg", ".png")):
                file_path = os.path.join(root, f)
                print(f"Inserting: {file_path}")
                insert_document(conn, file_path, category="TestLoad", status="Processed")

    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, category, status, last_modified FROM documents ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()

    print("\nLast 10 documents in DB:")
    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    main()

# end of script