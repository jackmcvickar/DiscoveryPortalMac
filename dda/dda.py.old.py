import os
import sqlite3
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract

DB_PATH = "/Users/jackmcvickar/DiscoveryPortalMac/Data/dda.db"

def extract_with_pdfminer(path):
    try:
        text = extract_text(path)
        return text.strip(), "pdfminer"
    except Exception as e:
        print(f"⚠️ pdfminer failed on {path}: {e}")
        return None, None

def extract_with_ocr(path):
    try:
        images = convert_from_path(path)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
        return text.strip(), "ocr"
    except Exception as e:
        print(f"⚠️ OCR failed on {path}: {e}")
        return None, None

def process_file(cur, file_id, path):
    # First try pdfminer
    text, source = extract_with_pdfminer(path)

    # Fallback to OCR if pdfminer fails or text is empty
    if not text:
        text, source = extract_with_ocr(path)

    if text:
        # Insert into extracts (FTS5 table)
        cur.execute(
            "INSERT INTO extracts (rowid, file_id, full_text) VALUES (?, ?, ?)",
            (file_id, file_id, text)
        )

        # Insert into extract_meta with timestamp
        cur.execute(
            "INSERT INTO extract_meta (file_id, source, created_at) VALUES (?, ?, datetime('now'))",
            (file_id, source)
        )

        print(f"✅ Extracted {path} via {source}")
    else:
        print(f"❌ No text extracted from {path}")

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Get all files
    cur.execute("SELECT id, path FROM files")
    files = cur.fetchall()

    total = len(files)
    print(f"📂 Found {total} files to process")

    for i, (file_id, path) in enumerate(files, start=1):
        if not os.path.exists(path):
            print(f"⚠️ Missing file: {path}")
            continue

        process_file(cur, file_id, path)

        if i % 100 == 0:
            conn.commit()
            print(f"💾 Committed {i}/{total} files")

    conn.commit()
    conn.close()
    print("🏁 Extraction complete")

if __name__ == "__main__":
    main()
