# dda/dashboard_api.py

from fastapi import FastAPI
import sqlite3

app = FastAPI(title="Discovery Portal Dashboard API")

DB_PATH = "/Users/jackmcvickar/DiscoveryPortalMac/Data/dda.db"

def get_db_conn():
    return sqlite3.connect(DB_PATH)

@app.get("/dashboard/categories")
def categories():
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT category, COUNT(*) FROM documents GROUP BY category")
        rows = cursor.fetchall()
        return {"categories": [{"category": cat, "count": cnt} for cat, cnt in rows]}
    finally:
        conn.close()

@app.get("/dashboard/status")
def status():
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) FROM documents GROUP BY status")
        rows = cursor.fetchall()
        return {"status": [{"status": st, "count": cnt} for st, cnt in rows]}
    finally:
        conn.close()

@app.get("/dashboard/recent")
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

@app.get("/dashboard/daily_counts")
def daily_counts():
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date(processed_at), COUNT(*)
            FROM documents
            WHERE processed_at IS NOT NULL
            GROUP BY date(processed_at)
            ORDER BY date(processed_at) DESC
        """)
        rows = cursor.fetchall()
        return {"daily_counts": [{"date": d, "count": c} for d, c in rows]}
    finally:
        conn.close()

@app.get("/dashboard/confidence_by_category")
def confidence_by_category():
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, AVG(confidence)
            FROM documents
            WHERE confidence IS NOT NULL
            GROUP BY category
        """)
        rows = cursor.fetchall()
        return {"confidence_by_category": [{"category": cat, "avg_confidence": avg} for cat, avg in rows]}
    finally:
        conn.close()

@app.get("/dashboard/top_owners")
def top_owners(limit: int = 5):
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT owner, COUNT(*)
            FROM documents
            WHERE owner IS NOT NULL
            GROUP BY owner
            ORDER BY COUNT(*) DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return {"top_owners": [{"owner": o, "count": c} for o, c in rows]}
    finally:
        conn.close()

# end of script