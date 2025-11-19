#!/usr/bin/env python3
# =============================================================================
# File: db_utils.py
# Purpose: Database helper functions for document ingestion pipeline
# =============================================================================

import sqlite3

def insert_document(records, db_conn_or_path):
    """
    Insert records into the documents table.

    Parameters
    ----------
    records : list of tuples
        Each tuple should be (filepath, category, status, filename).
    db_conn_or_path : sqlite3.Connection or str
        Either an open SQLite connection or a path to the database file.
    """
    if isinstance(db_conn_or_path, sqlite3.Connection):
        conn = db_conn_or_path
        close_after = False
    else:
        conn = sqlite3.connect(db_conn_or_path)
        close_after = True

    for filepath, category, status, filename in records:
        conn.execute(
            """
            INSERT INTO documents (filepath, category, status, filename)
            VALUES (?, ?, ?, ?)
            """,
            (filepath, category, status, filename),
        )
    conn.commit()
    if close_after:
        conn.close()


# Alias for backward compatibility with tests
def insert_into_db(records, db_conn_or_path):
    return insert_document(records, db_conn_or_path)


def fetch_all_documents(db_conn_or_path):
    """Return all documents from the database."""
    if isinstance(db_conn_or_path, sqlite3.Connection):
        conn = db_conn_or_path
        close_after = False
    else:
        conn = sqlite3.connect(db_conn_or_path)
        close_after = True

    rows = conn.execute("SELECT * FROM documents").fetchall()
    if close_after:
        conn.close()
    return rows


def delete_document_by_path(filepath, db_conn_or_path):
    """Delete a document record by its filepath."""
    if isinstance(db_conn_or_path, sqlite3.Connection):
        conn = db_conn_or_path
        close_after = False
    else:
        conn = sqlite3.connect(db_conn_or_path)
        close_after = True

    conn.execute("DELETE FROM documents WHERE filepath=?", (filepath,))
    conn.commit()
    if close_after:
        conn.close()


def update_document_status(filepath, status, db_conn_or_path):
    """Update the status of a document."""
    if isinstance(db_conn_or_path, sqlite3.Connection):
        conn = db_conn_or_path
        close_after = False
    else:
        conn = sqlite3.connect(db_conn_or_path)
        close_after = True

    conn.execute("UPDATE documents SET status=? WHERE filepath=?", (status, filepath))
    conn.commit()
    if close_after:
        conn.close()

# end of script