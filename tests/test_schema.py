import sqlite3
import os
import tempfile
import pytest
from dda.db import schema

def test_ensure_schema_adds_columns():
    # Create temp DB
    db_fd, db_path = tempfile.mkstemp()
    conn = sqlite3.connect(db_path)

    # Let ensure_schema create the full canonical schema
    schema.ensure_schema(conn)

    # Verify expected columns exist
    cursor = conn.execute("PRAGMA table_info(documents);")
    cols = [row[1] for row in cursor.fetchall()]
    assert "status" in cols
    assert "tags" in cols
    assert "hash" in cols
    assert "filepath" in cols

    conn.close()
    os.close(db_fd)
    os.remove(db_path)

# end of script