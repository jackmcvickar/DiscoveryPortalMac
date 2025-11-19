#!/usr/bin/env python3
# =============================================================================
# File: test_batch_pipeline.py
# Purpose: Validate batch pipeline integration
# =============================================================================

import sqlite3
from dda.db import schema
from dda.batch_pipeline import process_folder

def test_process_folder_inserts_multiple_docs(tmp_path):
    # Setup DB
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(db_file)
    schema.ensure_schema(conn)
    conn.close()

    # Create two dummy PDF files
    f1 = tmp_path / "file1.pdf"
    f2 = tmp_path / "file2.pdf"
    f1.write_text("Fake PDF content 1")
    f2.write_text("Fake PDF content 2")

    # Run batch pipeline
    conn = sqlite3.connect(db_file)
    process_folder(str(tmp_path), conn)

    # Verify insertion
    cursor = conn.cursor()
    cursor.execute("SELECT category, status FROM documents")
    rows = cursor.fetchall()
    # Expect at least 2 rows, since both files should be inserted
    assert len(rows) >= 2
    for _, status in rows:
        assert status in ("indexed", "error")
    conn.close()

# end of script