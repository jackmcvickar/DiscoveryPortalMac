# migrate_add_columns.py
# =============================================================================
# Purpose: Add owner, category, and period columns to documents table
# =============================================================================

import sqlite3

def migrate(db_path="./Data/dda.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Add new columns if they don't exist
    for column in ["owner TEXT", "category TEXT", "period TEXT"]:
        try:
            cur.execute(f"ALTER TABLE documents ADD COLUMN {column};")
            print(f"Added column: {column}")
        except sqlite3.OperationalError:
            print(f"Column already exists: {column}")

    conn.commit()
    conn.close()
    print("✅ Migration complete: owner, category, period columns ensured.")

if __name__ == "__main__":
    migrate()

# end of script