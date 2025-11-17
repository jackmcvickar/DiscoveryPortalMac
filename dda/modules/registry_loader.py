import sqlite3
import pandas as pd

DB_PATH = "Data/dda.db"
EXCEL_PATH = "Docs/McVickar Financial Summary.xlsx"

def load_registry():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS accounts_registry")
    cursor.execute("""
        CREATE TABLE accounts_registry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT,
            account_number TEXT,
            account_type TEXT,
            owner TEXT,
            status TEXT,
            notes TEXT
        )
    """)

    # Read first sheet
    df = pd.read_excel(EXCEL_PATH, sheet_name=0)

    for _, row in df.iterrows():
        account_name = str(row.get("Account", "")).strip()
        account_number = str(row.get("Account Number", "")).strip()
        account_type = str(row.get("Account Type", "")).strip()
        owner = str(row.get("Responsible to Pay", "")).strip()
        status = str(row.get("Sort", "")).strip()  # or another column for status
        notes = str(row.get("Notes", "")).strip()

        if account_name:  # skip blanks
            cursor.execute("""
                INSERT INTO accounts_registry
                (account_name, account_number, account_type, owner, status, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (account_name, account_number, account_type, owner, status, notes))

    conn.commit()
    conn.close()
    print("✅ Registry loaded from spreadsheet.")

if __name__ == "__main__":
    load_registry()
# end of script