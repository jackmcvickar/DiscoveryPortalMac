import os

def classify_document(filepath):
    parts = filepath.split(os.sep)
    category, account_id = "general", None

    for i, p in enumerate(parts):
        pl = p.lower()
        if "credit card" in pl:
            category = "Credit Cards"
            if i + 1 < len(parts):
                account_id = parts[i + 1]
            break
        elif "bank account" in pl:
            category = "Bank Accounts"
            if i + 1 < len(parts):
                account_id = parts[i + 1]
            break
        elif "loan" in pl:
            category = "Loans"
            if i + 1 < len(parts):
                account_id = parts[i + 1]
            break

    filename = os.path.basename(filepath)
    status = "Error" if "error" in filename.lower() else "Processed"
    return status, category, account_id

# end of script