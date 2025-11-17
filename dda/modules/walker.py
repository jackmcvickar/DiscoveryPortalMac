import os
from dda.modules.classifier import classify_document

def walk_documents(docs_path):
    records = []
    for root, dirs, files in os.walk(docs_path):
        # Skip unwanted dirs
        if "venv" in root or "__pycache__" in root:
            continue
        for fname in files:
            # Skip hidden/system files
            if fname.startswith("."):
                continue
            # Skip known junk extensions
            if fname.lower().endswith((".db", ".sql", ".py", ".pyc")):
                continue
            # Accept documents and scanned images
            if not fname.lower().endswith((
                ".pdf", ".docx", ".txt", ".jpg", ".jpeg", ".png", ".tiff"
            )):
                continue

            filepath = os.path.join(root, fname)
            status, category, account_id = classify_document(filepath)
            records.append((filepath, category, status, account_id))
    return records

# end of script