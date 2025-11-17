import sqlite3
from dda.modules import db_utils

def test_loader_integration(tmp_path):
    # Setup DB
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(db_file)
    conn.execute("CREATE TABLE documents (id INTEGER PRIMARY KEY, filepath TEXT, status TEXT, filename TEXT)")
    conn.commit()
    conn.close()

    # Insert a dummy record directly
    records = [(str(db_file), "general", "Processed", None)]
    db_utils.insert_into_db(records, str(db_file))

    # Verify row landed
    conn = sqlite3.connect(db_file)
    rows = conn.execute("SELECT filename, status FROM documents").fetchall()
    conn.close()
    assert len(rows) > 0
# end of script