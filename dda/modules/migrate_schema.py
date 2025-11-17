import sqlite3

DB_PATH = "Data/dda.db"

# Expected schema fields for documents table
EXPECTED_COLUMNS = {
    "filepath": "TEXT",
    "account_id": "TEXT",
    "account_number_last4": "TEXT",
    "owner": "TEXT",
    "period": "TEXT",
    "filesize": "INTEGER",
    "hash": "TEXT",
    "last_modified": "TEXT",
    "category": "TEXT",
    "confidence": "REAL",
    "year": "TEXT"   # new column we added
}

def migrate_documents_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get current columns
    cursor.execute("PRAGMA table_info(documents)")
    existing_cols = {row[1] for row in cursor.fetchall()}

    for col, col_type in EXPECTED_COLUMNS.items():
        if col not in existing_cols:
            try:
                cursor.execute(f"ALTER TABLE documents ADD COLUMN {col} {col_type};")
                print(f"✅ Added missing column: {col} ({col_type})")
            except sqlite3.OperationalError as e:
                print(f"⚠️ Could not add {col}: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_documents_table()
    print("📦 Schema migration complete.")
# end of script