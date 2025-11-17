import os
import configparser
import csv
import sqlite3
from dda.modules.logger import setup_logger

def load_config():
    config = configparser.ConfigParser()
    # Go up one directory from modules/ to reach dda/config.ini
    config.read(os.path.join(os.path.dirname(__file__), "..", "config.ini"))
    return config

def export_summary(results):
    """
    Export classification results to a CSV file in outputs_path.
    results: list of tuples (document_path, category)
    """
    cfg = load_config()
    outputs_path = cfg["paths"]["outputs_path"]
    db_path = cfg["paths"]["db_path"]
    docs_root = cfg["paths"]["docs_path"]
    os.makedirs(outputs_path, exist_ok=True)

    summary_file = os.path.join(outputs_path, "final_status_summary.csv")
    logger = setup_logger("report_generator")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    with open(summary_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["FileID", "Document", "Category", "DB_Status"])

        for doc, category in results:
            # Normalize to relative path (relative to docs_root)
            try:
                doc_rel = os.path.relpath(doc, start=docs_root)
            except Exception:
                doc_rel = doc  # fallback

            file_id, status = "N/A", "N/A"
            try:
                cur.execute("SELECT id, status FROM documents WHERE path = ?", (doc_rel,))
                row = cur.fetchone()
                if row:
                    file_id, status = row
            except Exception as e:
                logger.error(f"DB lookup failed for {doc_rel}: {e}")
                file_id, status = "Error", "Error"

            writer.writerow([file_id, doc_rel, category, status])
            logger.info(f"Wrote result for {doc_rel} as {category} (DB status={status})")

    conn.close()
    print(f"📑 Final status summary exported to {summary_file}")

def main():
    # Example usage: dummy results
    results = [
        ("/Users/jackmcvickar/DiscoveryPortalMac/Docs/invoice1.pdf", "financial"),
        ("/Users/jackmcvickar/DiscoveryPortalMac/Docs/contract1.pdf", "legal"),
    ]
    export_summary(results)

if __name__ == "__main__":
    main()
# end of script