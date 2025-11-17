import os
import sqlite3
import hashlib
import re
from datetime import datetime

DB_PATH = "Data/dda.db"

def classify_category(filepath: str) -> str:
    """Classify a document into a category based on its filepath/filename."""
    fp = filepath.lower()
    if "paystub" in fp or "payroll" in fp:
        return "Pay Stubs"
    elif "bank" in fp or "statement" in fp:
        return "Bank Statements"
    elif "credit" in fp or "card" in fp:
        return "Credit Cards"
    elif "tax" in fp or "1040" in fp or "return" in fp:
        return "Tax Returns"
    else:
        return "Other"

def extract_period(filename: str) -> str | None:
    """
    Extract a YYYY-MM period from filenames like:
    - 20220225_BANK_credit_card.pdf
    - 2024-04-26_statement.pdf
    - 202403_BANK.pdf
    """
    # Match YYYYMMDD or YYYY-MM-DD or YYYYMM
    match = re.search(r"(20\d{2})[-_]?(\d{2})", filename)
    if match:
        year, month = match.groups()
        return f"{year}-{month}"
    return None

def file_hash(filepath: str) -> str:
    """Generate SHA256 hash of a file for integrity tracking."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def extract_documents(root_dir="Docs"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS documents")
    cursor.execute(
        """
        CREATE TABLE documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            account_id TEXT,
            owner TEXT,
            period TEXT,
            confidence REAL,
            filepath TEXT,
            filesize INTEGER,
            hash TEXT,
            last_modified TEXT
        )
        """
    )

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            filesize = os.path.getsize(filepath)
            last_modified = datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
            filehash = file_hash(filepath)

            # Derive account_id and owner from folder structure
            account_id = os.path.basename(os.path.dirname(filepath))
            owner = os.path.basename(os.path.dirname(os.path.dirname(filepath)))

            # Extract period from filename
            period = extract_period(filename)

            category = classify_category(filepath)
            confidence = 1.0  # placeholder, can refine later

            cursor.execute(
                """
                INSERT INTO documents
                (category, account_id, owner, period, confidence, filepath, filesize, hash, last_modified)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (category, account_id, owner, period, confidence, filepath, filesize, filehash, last_modified),
            )

    conn.commit()
    conn.close()
    print("✅ Extraction complete, documents table rebuilt.")

if __name__ == "__main__":
    extract_documents()
# end of script