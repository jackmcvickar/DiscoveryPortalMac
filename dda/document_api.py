# dda/document_api.py

from fastapi import FastAPI
import sqlite3

app = FastAPI(title="Discovery Portal Document API")

DB_PATH = "/Users/jackmcvickar/DiscoveryPortalMac/Data/dda.db"

def get_db_conn():
    return sqlite3.connect(DB_PATH)

@app.get("/documents/categories")
def categories():
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT category, COUNT(*) FROM documents GROUP BY category")
        rows = cursor.fetchall()
        return {"categories": [{"category": cat, "count": cnt} for cat, cnt in rows]}
    finally:
        conn.close()

@app.get("/documents/status")
def status():
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) FROM documents GROUP BY status")
        rows = cursor.fetchall()
        return {"status": [{"status": st, "count": cnt} for st, cnt in rows]}
    finally:
        conn.close()

@app.get("/documents/recent")
def recent(limit: int = 10):
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT filename, category, status, processed_at
            FROM documents
            ORDER BY processed_at DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return {"recent_documents": [
            {"filename": fn, "category": cat, "status": st, "processed_at": ts}
            for fn, cat, st, ts in rows
        ]}
    finally:
        conn.close()

@app.get("/documents/owner/{owner}")
def documents_by_owner(owner: str):
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT filename, category, status, processed_at
            FROM documents
            WHERE owner = ?
            ORDER BY processed_at DESC
        """, (owner,))
        rows = cursor.fetchall()
        return {"documents": [
            {"filename": fn, "category": cat, "status": st, "processed_at": ts}
            for fn, cat, st, ts in rows
        ]}
    finally:
        conn.close()

# end of script