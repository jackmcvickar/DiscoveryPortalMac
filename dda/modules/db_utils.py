import sqlite3, os, time

def insert_into_db(records, db_path):
    print(f"📂 Inserting into DB at: {db_path}")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(documents)")
    cols = [row[1] for row in cur.fetchall()]

    for filepath, category, status, account_id in records:
        filename = os.path.basename(filepath)
        try:
            stat = os.stat(filepath)
            filesize = stat.st_size
            last_modified = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime))
        except FileNotFoundError:
            filesize, last_modified = None, None

        year = None
        for p in filepath.split(os.sep):
            if p.isdigit() and len(p) == 4:
                year = p
                break

        row = {
            "category": category,
            "account_id": account_id,
            "status": status,
            "filename": filename,
            "filepath": filepath,
            "filesize": filesize,
            "last_modified": last_modified,
            "year": year,
            "owner": "Jack",
            "confidence": 1.0,
        }

        valid_cols = {k: v for k, v in row.items() if k in cols}
        placeholders = ", ".join(["?"] * len(valid_cols))
        colnames = ", ".join(valid_cols.keys())

        print(f"📝 Inserting row: {valid_cols}")
        cur.execute(f"INSERT INTO documents ({colnames}) VALUES ({placeholders})", tuple(valid_cols.values()))

    conn.commit()
    conn.close()
# end of script