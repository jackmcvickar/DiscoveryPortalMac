#!/usr/bin/env python3
# =============================================================================
# File: test_pipeline.py
# Purpose: Validate single-document pipeline integration
# =============================================================================

import sqlite3
from dda.db import schema
from dda.pipeline import process_document

def test_process_document_inserts_into_db(tmp_path):
    # Setup DB
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(db_file)
    schema.ensure_schema(conn)
    conn.close()

    # Create a dummy PDF file
    sample_pdf = tmp_path / "sample.pdf"
    sample_pdf.write_text("Fake PDF content")

    # Run pipeline
    conn = sqlite3.connect(db_file)
    process_document(str(sample_pdf), conn)

    # Verify insertion
    cursor = conn.cursor()
    cursor.execute("SELECT category, status FROM documents")
    rows = cursor.fetchall()
    assert len(rows) == 1
    assert rows[0][1] in ("indexed", "error")
    conn.close()

# end of script