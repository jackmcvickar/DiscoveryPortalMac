# dda/dashboard_queries.py

import sqlite3
from typing import List, Dict

def get_category_counts(db_conn) -> Dict[str, int]:
    """
    Return a dictionary of document counts grouped by category.
    """
    cursor = db_conn.cursor()
    cursor.execute("SELECT category, COUNT(*) FROM documents GROUP BY category")
    results = cursor.fetchall()
    return {category: count for category, count in results}

def get_status_counts(db_conn) -> Dict[str, int]:
    """
    Return a dictionary of document counts grouped by status.
    """
    cursor = db_conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM documents GROUP BY status")
    results = cursor.fetchall()
    return {status: count for status, count in results}

def get_recent_documents(db_conn, limit: int = 10) -> List[Dict]:
    """
    Return the most recent documents processed, with filename, category, status, and timestamp.
    """
    cursor = db_conn.cursor()
    cursor.execute(
        """
        SELECT filename, category, status, processed_at
        FROM documents
        ORDER BY processed_at DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cursor.fetchall()
    return [
        {"filename": fn, "category": cat, "status": st, "processed_at": ts}
        for fn, cat, st, ts in rows
    ]

def get_documents_by_owner(db_conn, owner: str) -> List[Dict]:
    """
    Return all documents belonging to a specific owner.
    """
    cursor = db_conn.cursor()
    cursor.execute(
        """
        SELECT filename, category, status, processed_at
        FROM documents
        WHERE owner = ?
        ORDER BY processed_at DESC
        """,
        (owner,),
    )
    rows = cursor.fetchall()
    return [
        {"filename": fn, "category": cat, "status": st, "processed_at": ts}
        for fn, cat, st, ts in rows
    ]

# end of script