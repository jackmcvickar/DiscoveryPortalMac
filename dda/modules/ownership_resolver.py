# ownership_resolver.py
# =============================================================================
# Purpose: Infer category, account/owner, and period from file path + name
#          Enhanced to group Pay Stubs by payroll source + last 4 digits
# =============================================================================

import re
from datetime import datetime
import hashlib

def normalize_period(date_str):
    """Normalize date strings into YYYY-MM format."""
    if re.match(r"20\d{2}-\d{2}", date_str):
        return date_str
    for fmt in ["%m-%d-%y", "%m-%d-%Y"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m")
        except ValueError:
            continue
    return None

def derive_account_id(filepath, category, owner=None):
    """
    Derive account_id for grouping.
    - Bank Statements: use folder name (already account_id).
    - Pay Stubs: payroll source + last 4 digits.
    - Tax Returns: fixed 'Joint'.
    """
    if category == "Bank Statements":
        return owner  # already account_id from folder

    if category == "Pay Stubs":
        # Payroll source from filename
        m = re.search(r"(EEPayroll|Employer[A-Za-z0-9]+)", filepath)
        payroll_source = m.group(1) if m else "Payroll"
        # Last 4 digits from filename
        digits = re.findall(r"\d{4}", filepath)
        suffix = digits[-1] if digits else hashlib.sha1(filepath.encode()).hexdigest()[:4]
        return f"{payroll_source}-{suffix}"

    if category == "Tax Returns":
        return "Joint"

    return None

def resolve_owner_account(filepath):
    parts = filepath.split("/")
    category = None
    account_id = None
    owner = None
    period = None
    confidence = 0.9

    # --- Bank Statements ---
    if "BankStatements" in parts:
        category = "Bank Statements"
        try:
            idx = parts.index("BankStatements")
            account_id = parts[idx+1]
        except Exception:
            confidence = 0.5
        m = re.search(r"(20\d{2}-\d{2})", filepath)
        if m:
            period = normalize_period(m.group(1))

    # --- Pay Stubs ---
    elif "PayStubs" in parts or "Paystubs" in parts:
        category = "Pay Stubs"
        try:
            idx = parts.index("PayStubs") if "PayStubs" in parts else parts.index("Paystubs")
            owner = parts[idx+1] if idx+1 < len(parts) else None
        except Exception:
            confidence = 0.5
        m = re.search(r"(20\d{2}-\d{2}|\d{2}-\d{2}-\d{2,4})", filepath)
        if m:
            period = normalize_period(m.group(1))
        account_id = derive_account_id(filepath, category, owner)

    # --- Tax Returns ---
    elif "TaxReturns" in parts:
        category = "Tax Returns"
        account_id = "Joint"
        m = re.search(r"(20\d{2})", filepath)
        if m:
            period = m.group(1)

    return {
        "category": category,
        "account_id": account_id,
        "owner": owner,
        "period": period,
        "confidence": confidence
    }

# end of script