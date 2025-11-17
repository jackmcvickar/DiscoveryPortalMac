# ownership_audit.py
# =============================================================================
# Purpose: Create audit trail table for ownership resolver
# =============================================================================

import sqlite3

def create_audit_table(db_path="./Data/dda.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ownership_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            filepath TEXT,
            inferred_owner TEXT,
            inferred_category TEXT,
            inferred_period TEXT,
            method TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Audit table created.")

if __name__ == "__main__":
    create_audit_table()

# end of script