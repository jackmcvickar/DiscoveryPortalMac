#!/usr/bin/env python3
# =============================================================================
# File: classifier.py
# =============================================================================

def classify_document(filepath):
    """Stub classifier: return (status, category, account_id)."""
    fname = filepath.lower()
    if "credit" in fname:
        return "indexed", "Credit Cards", "USAA"
    elif "error" in fname:
        return "error", "Error Report", None
    else:
        return "indexed", "General", None

# end of script