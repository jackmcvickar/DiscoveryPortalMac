import sqlite3, tempfile, os
from dda.modules import db_utils

def test_insert_into_db_creates_rows(tmp_path):
    db_file = tmp_path / "test.sqlite"
    conn = sqlite3.connect(db_file)
    conn.execute("CREATE TABLE documents (id INTEGER PRIMARY KEY, category TEXT, account_id TEXT, status TEXT, filename TEXT, filepath TEXT, year TEXT, owner TEXT, confidence REAL)")
    conn.commit()
    conn.close()

    records = [(str(db_file), "general", "Processed", None)]
    db_utils.insert_into_db(records, str(db_file))

    conn = sqlite3.connect(db_file)
    rows = conn.execute("SELECT filename, status FROM documents").fetchall()
    conn.close()
    assert len(rows) > 0
# end of script