import sqlite3
import tempfile
import os
from dda import indexer
from dda.db import schema

def test_ingest_directory_flags_duplicates(tmp_path):
    # Create two identical files
    f1 = tmp_path / "file1.txt"
    f2 = tmp_path / "file2.txt"
    f1.write_text("duplicate content")
    f2.write_text("duplicate content")

    # Create temp DB and apply full schema
    db_fd, db_path = tempfile.mkstemp()
    conn = sqlite3.connect(db_path)
    schema.ensure_schema(conn)

    cfg = {"enable_ocr": False}
    indexer.ingest_directory(conn, str(tmp_path), [], [], cfg)

    rows = conn.execute("SELECT is_duplicate FROM documents").fetchall()
    # One should be 0, the other 1
    assert sorted([r[0] for r in rows]) == [0, 1]

    conn.close()
    os.close(db_fd)
    os.remove(db_path)

# end of script