import sqlite3
import csv

DB_PATH = "Data/dda.db"

# Whitelist of categories we care about
VALID_CATEGORIES = {"Pay Stubs", "Bank Statements", "Credit Cards", "Tax Returns"}

# Expanded blacklist of obvious system/junk names
SYSTEM_NAMES = {
    "__pycache__", "pycparser", "openpyxl", "matplotlib", "dist-info",
    "styles","caches","_in_process","rich","contrib","_securetransport","packages",
    "backports","resolvers","babel","messages","locale-data","localtime","sklearn",
    "torch","scipy","numpy","joblib","csvkit","tqdm","pdfminer","reportlab","pypdf",
    "widgets","fonts","yaml","html","css","js","qt_editor","mpl-data","sample_data",
    "tests","examples","docs","docx","text","images","datasets","openml","id_",
    "arff","matlab","lobpcg","fftpack","signal","stats","special","spatial",
    "transform","utilities","convert","generic","constants","backend","cloudpickle",
    "loky","xlrd","PySimpleGUI","kiwisolver","tri","axes","style","ticks","shapes",
    "scales","barcode","graphics","samples","annotations","isoschematron","libxslt",
    "libexslt","qhull_src","platypus","afm","ttf","stylelib","pdf2image"
}

def is_valid_account(account_id, category):
    if category not in VALID_CATEGORIES:
        return False
    if not account_id or len(account_id) < 3:
        return False
    if account_id.isdigit():
        return False
    if any(sys in account_id.lower() for sys in SYSTEM_NAMES):
        return False
    return True

def export_overrides():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT account_id, category FROM documents")
    accounts = cursor.fetchall()

    override_file = "reports/account_overrides.csv"
    exported, skipped = 0, 0

    with open(override_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "raw_account", "raw_category",
            "preferred_name", "preferred_category",
            "last4", "preferred_owner"
        ])
        for account_id, category in accounts:
            if is_valid_account(account_id, category):
                writer.writerow([account_id, category, "", "", "", ""])
                exported += 1
            else:
                skipped += 1

    conn.close()
    print(f"✅ Exported {exported} accounts to {override_file}")
    print(f"⚠️ Skipped {skipped} system/junk entries")

def import_overrides():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS account_overrides")
    cursor.execute(
        """
        CREATE TABLE account_overrides (
            raw_account TEXT,
            raw_category TEXT,
            preferred_name TEXT,
            preferred_category TEXT,
            last4 TEXT,
            preferred_owner TEXT
        )
        """
    )

    override_file = "reports/account_overrides.csv"
    with open(override_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                "INSERT INTO account_overrides VALUES (?, ?, ?, ?, ?, ?)",
                (
                    row["raw_account"],
                    row["raw_category"],
                    row["preferred_name"],
                    row["preferred_category"],
                    row["last4"],
                    row["preferred_owner"],
                ),
            )

    conn.commit()
    conn.close()
    print("✅ Overrides imported into DB")

if __name__ == "__main__":
    # First run export_overrides() to create the CSV
    export_overrides()
    # After editing the CSV, run import_overrides() to load changes
    # import_overrides()

# end of script