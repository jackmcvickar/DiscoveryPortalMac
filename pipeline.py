# pipeline.py

import os
import sqlite3
import datetime
import hashlib
from collections import defaultdict
from log_utils import write_log

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
LOGS_PATH = config["logs_path"]

def get_db_conn():
    return sqlite3.connect(DB_PATH)

def file_hash(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def parse_file(file_path: str) -> str:
    # Stub parser
    return f"Parsed content for {os.path.basename(file_path)}"

def classify_content(content: str) -> str:
    # Stub classifier
    return "Uncategorized"

def extract_metadata(file_path: str, content: str) -> dict:
    # Stub metadata extractor
    return {
        "owner": None,
        "account_id": None,
        "period": None,
        "year": str(datetime.datetime.now().year),
        "confidence": 0.95,
    }

def upsert_document(db_conn, file_path: str, content: str, category: str, metadata: dict, status: str = "Processed"):
    filename = os.path.basename(file_path)
    processed_at = datetime.datetime.now().isoformat()
    filehash = file_hash(file_path)

    cursor = db_conn.cursor()
    cursor.execute("SELECT id, hash FROM documents WHERE filepath = ?", (file_path,))
    row = cursor.fetchone()

    if row:
        existing_id, existing_hash = row
        if existing_hash == filehash:
            return f"Unchanged: {filename}"
        else:
            cursor.execute(
                """
                UPDATE documents
                SET category=?, filename=?, status=?, confidence=?, last_modified=?, year=?, owner=?, account_id=?, period=?, hash=?
                WHERE id=?
                """,
                (
                    category,
                    filename,
                    status,
                    metadata.get("confidence"),
                    processed_at,
                    metadata.get("year"),
                    metadata.get("owner"),
                    metadata.get("account_id"),
                    metadata.get("period"),
                    filehash,
                    existing_id,
                ),
            )
            db_conn.commit()
            return f"Updated: {filename}"
    else:
        cursor.execute(
            """
            INSERT INTO documents (
                category, filepath, filename, status, confidence, last_modified, year, owner, account_id, period, hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                category,
                file_path,
                filename,
                status,
                metadata.get("confidence"),
                processed_at,
                metadata.get("year"),
                metadata.get("owner"),
                metadata.get("account_id"),
                metadata.get("period"),
                filehash,
            ),
        )
        db_conn.commit()
        return f"Inserted: {filename}"

def run_pipeline():
    print("=== Pipeline Sanity Check ===")
    print(f"DB_PATH: {DB_PATH}")
    print(f"SOURCE_DIR: {SOURCE_DIR}")
    print(f"LOGS_PATH: {LOGS_PATH}")
    print("=============================")

    conn = get_db_conn()
    details = []
    category_counts = defaultdict(lambda: {"Inserted": 0, "Updated": 0, "Unchanged": 0})

    for root, _, files in os.walk(SOURCE_DIR):
        for f in files:
            if f.lower().endswith((".pdf", ".jpg", ".png")):
                file_path = os.path.join(root, f)
                content = parse_file(file_path)
                category = classify_content(content)
                metadata = extract_metadata(file_path, content)

                result = upsert_document(conn, file_path, content, category, metadata)
                details.append(f"{result} ({category})")
                print(f"{result} ({category})")

                if result.startswith("Inserted"):
                    category_counts[category]["Inserted"] += 1
                elif result.startswith("Updated"):
                    category_counts[category]["Updated"] += 1
                elif result.startswith("Unchanged"):
                    category_counts[category]["Unchanged"] += 1

    summary_lines = ["Pipeline complete."]
    for cat, counts in category_counts.items():
        summary_lines.append(
            f"{cat}: Inserted {counts['Inserted']}, Updated {counts['Updated']}, Unchanged {counts['Unchanged']}"
        )
    summary = "\n".join(summary_lines)

    print("\n" + summary)
    write_log(LOGS_PATH, summary, details)
    conn.close()

if __name__ == "__main__":
    run_pipeline()

# end of script