#!/usr/bin/env python3
# =============================================================================
# File: test_document_loader.py
# Purpose: Integration test for document loader and DB utilities
# =============================================================================

import sqlite3
from dda.db import schema
from dda.modules import db_utils

def test_loader_integration(tmp_path):
    # Setup DB
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(db_file)
    schema.ensure_schema(conn)
    conn.close()

    # Insert a dummy record directly
    records = [(str(db_file), "general", "indexed", "dummy.pdf")]
    db_utils.insert_into_db(records, str(db_file))

    conn = sqlite3.connect(db_file)
    rows = conn.execute("SELECT category, status FROM documents").fetchall()
    assert rows[0][0] == "general"
    assert rows[0][1] == "indexed"
    conn.close()

# end of script