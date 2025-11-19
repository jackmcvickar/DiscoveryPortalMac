import sqlite3
import os

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "..", "schema.sql")

def ensure_schema(conn):
    """Bootstrap schema and add missing columns safely for SQLite."""
    with open(SCHEMA_FILE, "r") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)

    cursor = conn.execute("PRAGMA table_info(documents);")
    cols = [row[1] for row in cursor.fetchall()]
    if "tags" not in cols:
        conn.execute("ALTER TABLE documents ADD COLUMN tags TEXT;")
    if "text_source" not in cols:
        conn.execute("ALTER TABLE documents ADD COLUMN text_source TEXT;")
    if "is_duplicate" not in cols:
        conn.execute("ALTER TABLE documents ADD COLUMN is_duplicate INTEGER DEFAULT 0;")

    conn.commit()

def upsert_document(conn, doc):
    sql = """
    INSERT INTO documents (category, filepath, filename, status, confidence,
                           last_modified, year, owner, account_id, period, hash, tags, text_source, is_duplicate)
    VALUES (:category, :filepath, :filename, :status, :confidence,
            :last_modified, :year, :owner, :account_id, :period, :hash, :tags, :text_source, :is_duplicate)
    ON CONFLICT(hash) DO UPDATE SET
        category=excluded.category,
        filepath=excluded.filepath,
        filename=excluded.filename,
        status=excluded.status,
        last_modified=excluded.last_modified,
        tags=excluded.tags,
        text_source=excluded.text_source,
        is_duplicate=excluded.is_duplicate;
    """
    conn.execute(sql, doc)

# end of script