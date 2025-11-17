import sqlite3
from pathlib import Path
from dda.modules.status_logger import print_status_summary, log_status_summary, export_final_summary, DB_PATH

def setup_db(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(db_file)
    conn.execute("CREATE TABLE documents (id INTEGER PRIMARY KEY, filepath TEXT, status TEXT, filename TEXT)")
    conn.execute("INSERT INTO documents (filepath, status, filename) VALUES ('a.pdf','processed','a.pdf')")
    conn.commit()
    conn.close()
    return db_file

def test_print_and_export(tmp_path, monkeypatch):
    monkeypatch.setattr("dda.modules.status_logger.DB_PATH", setup_db(tmp_path))
    rows = print_status_summary()
    assert any(r[0] == "processed" for r in rows)
    log_status_summary(rows)
    export_final_summary()
    assert Path("reports/final_status_summary.csv").exists()
# end of script