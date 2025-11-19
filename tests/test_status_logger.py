#!/usr/bin/env python3
# =============================================================================
# File: test_status_logger.py
# Purpose: Validate status logger functions against canonical schema
# =============================================================================

import sqlite3
from dda.db import schema
from dda.modules.status_logger import print_status_summary, export_final_summary

def setup_db(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(db_file)
    schema.ensure_schema(conn)   # <-- use canonical schema
    conn.close()
    return str(db_file)

def test_print_and_export(tmp_path, monkeypatch):
    db_path = setup_db(tmp_path)
    monkeypatch.setattr("dda.modules.status_logger.DB_PATH", db_path)

    # Should not raise OperationalError now
    rows = print_status_summary()
    assert isinstance(rows, list) or rows is None

    conn = sqlite3.connect(db_path)
    export_final_summary(conn)
    conn.close()

# end of script